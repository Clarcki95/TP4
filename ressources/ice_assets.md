# Images de glace

Générées avec l'outil intégré `image_gen`, puis redimensionnées avec Pillow.

- `bricks/ice_brick.webp` : 400 × 200, affichée en 100 × 50 dans le jeu.
- `backgrounds/game_bg_ice.png` : 1200 × 750, affichée en 1600 × 1000.

## Prompt de la texture

```text
Use case: stylized-concept
Asset type: raster texture for an ice brick in a 2D Breakout arcade game, displayed at 100 by 50 pixels.
Primary request: a beautiful blue ice brick texture filling the entire rectangular image edge to edge. Front-facing orthographic flat rectangular face, frosty white crystalline borders and beveled icy edges, rich cyan blue translucent center, a few bold branching cracks and trapped bubbles. Readable high-contrast large forms at tiny game sprite scale. Crisp stylized game art with subtle realistic ice detail. Entire image is ice material, no margin, no surrounding scene, no perspective, no text, no snowflake icon, no letters, no watermark. Landscape 2:1 composition.
```

## Prompt du fond givré

Image source : `backgrounds/game_bg.gif`.

```text
Use case: lighting-weather
Asset type: frozen variant of the supplied dark background for a 2D Breakout game.
Input image: the local game_bg.gif is the edit target.
Primary request: cover this exact background with an icy frost effect. Preserve the dark tiled grid, its layout and vignette, keep the center dark navy and low contrast so a blue ball and white paddle remain readable. Add cyan blue translucent ice veins and white crystalline hoarfrost primarily at all four outer edges and corners, fading softly towards the middle; delicate sparse frosty cracks over the central grid. Flat front-facing game background, no perspective, no text, no objects, no falling snow, no UI. Landscape 8:5 image. The frozen state must be immediately apparent, but gameplay readability is paramount.
```
