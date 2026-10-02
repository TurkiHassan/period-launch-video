import sys
from PIL import Image
files=sys.argv[2:]; out=sys.argv[1]; n=len(files); cols=min(3,n); rows=(n+cols-1)//cols; s=480
sh=Image.new("RGB",(cols*s+(cols-1)*8,rows*s+(rows-1)*8),(255,255,255))
for i,f in enumerate(files): sh.paste(Image.open(f).convert("RGB").resize((s,s),Image.LANCZOS),((i%cols)*(s+8),(i//cols)*(s+8)))
sh.save(out)
