from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw, ImageFont
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
WORK = ROOT / '_work'
SHOTS = WORK / 'screenshots'
SHOTS.mkdir(exist_ok=True)
report = {'console_errors': [], 'network_requests': [], 'slides': [], 'checks': {}}
with sync_playwright() as p:
    browser = p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe', headless=True)
    page = browser.new_page(viewport={'width': 1920, 'height': 1142}, device_scale_factor=1)
    page.on('pageerror', lambda e: report['console_errors'].append(str(e)))
    page.on('request', lambda r: report['network_requests'].append(r.url) if r.url.startswith(('http:', 'https:')) else None)
    page.goto((ROOT/'成果展示.html').as_uri(), wait_until='load')
    page.emulate_media(reduced_motion='reduce')
    report['checks']['slide_count'] = page.locator('.deck > .slide').count()
    for n in range(1,11):
        page.evaluate('(n) => location.hash = "#/" + n', n)
        page.wait_for_function('(n) => document.querySelectorAll(".deck > .slide")[n-1].classList.contains("is-active")', arg=n)
        page.wait_for_timeout(120)
        dimensions = page.evaluate('''() => {
          const slide=document.querySelector('.deck > .slide.is-active'), main=slide.querySelector('.slide-main');
          const r=main.getBoundingClientRect();
          const escaped=[...main.querySelectorAll('p,table,.panel,.flow,.network,.step,.condition,.interface-line,.img-frame,.path,.merge,.callout,.formula,.metric,.scope-line,.net-node,h3,h4')].map(el=>{
            const b=el.getBoundingClientRect();
            if(b.bottom>r.bottom+2||b.right>r.right+2||b.left<r.left-2||b.top<r.top-2||el.scrollWidth>el.clientWidth+2||el.scrollHeight>el.clientHeight+2){
              return {tag:el.tagName,class:el.className,text:el.textContent.trim().slice(0,70),bottom:Math.round(b.bottom-r.bottom),width:el.clientWidth,scrollWidth:el.scrollWidth,height:el.clientHeight,scrollHeight:el.scrollHeight};
            }
          }).filter(Boolean);
          return {title:slide.dataset.title, main_height:main.clientHeight, escaped, images:[...slide.querySelectorAll('img')].map(img=>({loaded:img.complete&&img.naturalWidth>0,width:img.clientWidth,height:img.clientHeight,fit:getComputedStyle(img).objectFit}))};
        }''')
        dimensions['page'] = n
        report['slides'].append(dimensions)
        page.locator('.deck').screenshot(path=str(SHOTS/f'{n:02}.png'))

    page.keyboard.press('Home')
    page.keyboard.press('ArrowRight')
    report['checks']['keyboard_next'] = page.evaluate('location.hash') == '#/2'
    page.locator('#next-slide').click()
    report['checks']['button_next'] = page.evaluate('location.hash') == '#/3'
    page.locator('#slide-select').select_option('6')
    report['checks']['select_jump'] = page.evaluate('location.hash') == '#/6'
    page.locator('.chapter-nav a[data-chapter="4"]').click()
    report['checks']['chapter_jump'] = page.evaluate('location.hash') == '#/4'
    page.locator('.slide.is-active .img-frame img').first.click()
    report['checks']['zoom_open'] = page.locator('#zoom-modal').evaluate('(e)=>e.classList.contains("open")')
    before=page.evaluate('location.hash')
    page.keyboard.press('ArrowRight')
    report['checks']['zoom_blocks_navigation'] = page.evaluate('location.hash')==before
    page.keyboard.press('Escape')
    report['checks']['zoom_close'] = not page.locator('#zoom-modal').evaluate('(e)=>e.classList.contains("open")')
    page.locator('#show-source').click()
    report['checks']['source_modal'] = page.locator('#source-modal').evaluate('(e)=>e.classList.contains("open")')
    page.keyboard.press('Escape')
    page.keyboard.press('o')
    report['checks']['overview_count'] = page.locator('.overview.open .thumb').count()
    page.locator('.overview.open .thumb').nth(7).click()
    report['checks']['overview_jump'] = page.evaluate('location.hash')=='#/8'
    page.keyboard.press('n')
    report['checks']['notes_open'] = page.locator('.notes-overlay').evaluate('(e)=>e.classList.contains("open")')
    page.keyboard.press('Escape')

    for label,width,height in [('laptop',1366,768),('mobile_landscape',844,390),('mobile_portrait',390,844)]:
        page.set_viewport_size({'width':width,'height':height})
        page.wait_for_timeout(150)
        for n in [1,4,9]:
            page.evaluate('(n)=>location.hash="#/"+n',n)
            page.wait_for_timeout(80)
            page.screenshot(path=str(SHOTS/f'{label}_{n:02}.png'))
        report['checks'][label] = page.evaluate('''() => {
          const d=document.querySelector('.deck').getBoundingClientRect(), t=document.querySelector('.deck-tools').getBoundingClientRect();
          return {canvas_visible:d.left>=-1&&d.top>=-1&&d.right<=innerWidth+1&&d.bottom<=t.top+2,body_overflow:document.documentElement.scrollWidth>innerWidth+1,tools_height:t.height};
        }''')
    browser.close()

manifest=json.loads((WORK/'sources.json').read_text(encoding='utf-8-sig'))
changed=[]
for filename,digest in manifest['source_hashes'].items():
    if hashlib.sha256(Path(filename).read_bytes()).hexdigest()!=digest:
        changed.append(filename)
report['checks']['source_files_unchanged']=not changed
report['changed_sources']=changed
(WORK/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')

font=ImageFont.truetype(r'C:\Windows\Fonts\msyh.ttc',18)
preview=Image.new('RGB',(1600,5*486),(247,249,252))
draw=ImageDraw.Draw(preview)
for i,slide in enumerate(report['slides']):
    x=(i%2)*800+16;y=(i//2)*486+10
    image=Image.open(SHOTS/f'{i+1:02}.png').convert('RGB')
    image.thumbnail((768,432),Image.Resampling.LANCZOS)
    preview.paste(image,(x,y))
    draw.text((x+4,y+440),f'{i+1:02}  {slide["title"]}',font=font,fill=(70,93,120))
preview.save(ROOT/'10页总览.png')
print(json.dumps(report,ensure_ascii=False,indent=2))
