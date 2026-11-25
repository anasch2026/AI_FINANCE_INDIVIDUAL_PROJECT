"""Create slide-content previews with bundled fonts (not a native Office render).

Reads the actual PowerPoint shapes, tables and text. Aptos/Calibri are substituted
with matplotlib's bundled DejaVu Sans. These images support layout review and do
not replace opening the final deck in the application used for the defence.
"""
from pathlib import Path
import importlib.util
import json
import math
from PIL import Image, ImageDraw, ImageFont
from pptx import Presentation
from pptx.enum.text import PP_ALIGN

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'capstone/previews'
DPI=120
EMU=914400


def main():
    OUT.mkdir(exist_ok=True)
    spec=importlib.util.find_spec('matplotlib')
    fonts=Path(spec.origin).resolve().parent/'mpl-data/fonts/ttf'
    deck=Presentation(ROOT/'capstone/presentation.pptx')
    def px(value):return round(value/EMU*DPI)
    def font(points,bold=False):return ImageFont.truetype(str(fonts/('DejaVuSans-Bold.ttf' if bold else 'DejaVuSans.ttf')),max(1,round(points*DPI/72)))
    def rgb(fill,default='#FFFFFF'):
        try:return '#'+str(fill.fore_color.rgb)
        except (AttributeError,TypeError,ValueError):return default
    def text_color(p,default='#25313C'):
        try:return '#'+str(p.font.color.rgb)
        except (AttributeError,TypeError,ValueError):return default
    def draw_frame(draw,frame,x,y,w,h,default_size=18):
        x+=px(frame.margin_left);y+=px(frame.margin_top)
        width=w-px(frame.margin_left)-px(frame.margin_right)
        for p in frame.paragraphs:
            if not p.text:continue
            size=p.font.size.pt if p.font.size else default_size
            face=font(size,bool(p.font.bold))
            lines=[];line=''
            for word in p.text.split():
                candidate=(line+' '+word).strip()
                if line and draw.textlength(candidate,font=face)>width:lines.append(line);line=word
                else:line=candidate
            if line:lines.append(line)
            height=math.ceil(size*DPI/72*1.12)
            for line in lines:
                dx=0
                if p.alignment==PP_ALIGN.RIGHT:dx=width-draw.textlength(line,font=face)
                elif p.alignment==PP_ALIGN.CENTER:dx=(width-draw.textlength(line,font=face))/2
                draw.text((x+dx,y),line,font=face,fill=text_color(p),anchor='lt')
                y+=height
            y+=(p.space_after.pt if p.space_after else 0)*DPI/72
    images=[]
    for number,slide in enumerate(deck.slides,1):
        image=Image.new('RGB',(px(deck.slide_width),px(deck.slide_height)),'white');draw=ImageDraw.Draw(image)
        for shape in slide.shapes:
            x,y,w,h=[px(getattr(shape,k)) for k in ['left','top','width','height']]
            if shape.has_table:
                table=shape.table;cy=y
                for row in table.rows:
                    cx=x;rh=px(row.height)
                    for j,cell in enumerate(row.cells):
                        cw=px(table.columns[j].width)
                        draw.rectangle((cx,cy,cx+cw,cy+rh),fill=rgb(cell.fill),outline='white',width=1)
                        draw_frame(draw,cell.text_frame,cx,cy+max(0,(rh-22*DPI/72)/3),cw,rh)
                        cx+=cw
                    cy+=rh
            elif shape.has_text_frame:
                try:
                    if shape.fill.type == 1:draw.rectangle((x,y,x+w,y+h),fill=rgb(shape.fill))
                except AttributeError:pass
                draw_frame(draw,shape.text_frame,x,y,w,h)
        image.save(OUT/f'slide-{number}.png');images.append(image)
    size=(800,450);montage=Image.new('RGB',(1600,900),'#E7EBEF')
    for i,im in enumerate(images):montage.paste(im.resize(size,Image.Resampling.LANCZOS),((i%2)*800,(i//2)*450))
    montage.save(OUT/'overview.png')
    (OUT/'README.txt').write_text('Previews of actual slide objects using bundled DejaVu Sans in place of Aptos. Not a native PowerPoint/LibreOffice rendering.\n')
    print('Saved four labelled slide-content previews; font-substitution scope documented.')


if __name__=='__main__':main()
