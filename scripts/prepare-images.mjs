import sharp from 'sharp';
import { mkdir, rm } from 'node:fs/promises';
const source=new URL('../public/images/',import.meta.url);
const output=new URL('../public/media/',import.meta.url);
await mkdir(output,{recursive:true});
const images=[['workshop-day','c6fuhuc6fuhuc6fu',1600],['workshop-night','5e3v2m5e3v2m5e3v',1600]];
await sharp(new URL('taylor-lang-stitched-comic-poster.webp',source).pathname).resize({width:1000,withoutEnlargement:true}).webp({quality:85}).toFile(new URL('poster.webp',output).pathname);
await Promise.all(images.map(async([name,id,width])=>{await sharp(new URL(`Gemini_Generated_Image_${id}.png`,source).pathname).resize({width,withoutEnlargement:true}).webp({quality:85}).toFile(new URL(`${name}.webp`,output).pathname);}));
await sharp(new URL('crew-youtube-v2.png',source).pathname).trim({background:'#000000',threshold:12}).resize({width:1800,withoutEnlargement:true}).webp({quality:85}).toFile(new URL('crew-youtube-v2.webp',output).pathname);
const legacyCharacterImages=['lang.webp','paye.webp','robot.webp','bird.webp'];
await Promise.all(legacyCharacterImages.map((file)=>rm(new URL(file,output),{force:true})));
const characterSource=new URL('4_characters_one_shot.png',source).pathname;
const characterCrops=[
  ['character-01',0,0],
  ['character-02',1040,0],
  ['character-03',0,1040],
  ['character-04',1040,1040],
];
await Promise.all(characterCrops.map(async([name,left,top])=>{
  await sharp(characterSource)
    .extract({left,top,width:1008,height:1008})
    .resize({width:720,height:720})
    .webp({quality:85})
    .toFile(new URL(`${name}.webp`,output).pathname);
}));
console.log('Prepared optimized WebP images, including four character panels.');
