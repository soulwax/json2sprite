import json
import os
import sys
from pathlib import Path

from PIL import Image


def render_sprite(sprite, pixel_size=16):
    grid = sprite["grid"]
    palette = sprite["palette"]
    h, w = len(grid), len(grid[0])
    img = Image.new("RGBA", (w, h), (0,0,0,0))
    for y,row in enumerate(grid):
        for x,ch in enumerate(row):
            color = palette.get(ch, "transparent")
            if color == "transparent":
                continue
            rgb = tuple(int(color[i:i+2],16) for i in (1,3,5))
            img.putpixel((x,y), rgb+(255,))
    return img.resize((w*pixel_size, h*pixel_size), Image.NEAREST)

def make_spritesheet(sprites, pixel_size=16, padding=4):
    rendered = [render_sprite(s,pixel_size) for s in sprites]
    widths, heights = zip(*(im.size for im in rendered))
    sheet = Image.new("RGBA", (sum(widths)+padding*(len(rendered)-1), max(heights)), (0,0,0,0))
    xoff=0
    for im in rendered:
        sheet.paste(im,(xoff,0),im)
        xoff += im.width+padding
    return sheet

def process_json_file(json_path, output_path):
    print(f"Processing {json_path} -> {output_path}", flush=True)
    with open(json_path,"r",encoding="utf-8") as f:
        data=json.load(f)
    if not isinstance(data,list):
        print("JSON root not a list, skipping", flush=True)
        return
    sheet=make_spritesheet(data)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output_path)
    print(f"Saved {output_path}", flush=True)

def process_folder(input_folder, output_folder):
    for root,_,files in os.walk(input_folder):
        for file in files:
            if file.lower().endswith(".json"):
                jpath=Path(root)/file
                rel=jpath.relative_to(input_folder).with_suffix(".png")
                opath=output_folder/rel
                process_json_file(jpath, opath)

def main():
    if len(sys.argv)!=2:
        print("Usage: python json2sprite.py <json_file_or_folder>")
        sys.exit(1)
    input_path=Path(sys.argv[1])
    output_root=Path("output")
    if input_path.is_file() and input_path.suffix.lower()==".json":
        process_json_file(input_path, output_root/(input_path.stem+".png"))
    elif input_path.is_dir():
        process_folder(input_path, output_root)
    else:
        print("Invalid input path")

if __name__=="__main__":
    main()