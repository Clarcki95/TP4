# Textures des briques

Textures générées avec l'outil intégré `image_gen`, en prenant `ice_brick.webp` comme référence de style. Chaque nouvelle image a été redimensionnée en 400 × 200 avec Pillow et est affichée en 100 × 50 dans le jeu. Les fichiers précédents sont conservés.

| Type | Fichier | Utilisation |
| --- | --- | --- |
| Normale | [brick_v2.webp](brick_v2.webp) | Chargée par la classe correspondante. |
| Accélératrice | [accelerator_brick_v2.webp](accelerator_brick_v2.webp) | Chargée par la classe correspondante. |
| Explosive | [explosive_brick_v2.webp](explosive_brick_v2.webp) | Chargée par la classe correspondante. |
| Indestructible | [undestructible_brick_v2.webp](undestructible_brick_v2.webp) | Chargée par la classe correspondante. |
| Duplicatrice | [duplicator_brick_v2.webp](duplicator_brick_v2.webp) | Texture prête ; classe de duplication pas encore implémentée. |
| Glace | [ice_brick.webp](ice_brick.webp) | Texture générée précédemment et conservée. |

Les prompts de la glace et du fond givré figurent dans [ice_assets.md](../ice_assets.md).

## Prompts complets

### Normale

```text
Use case: stylized-concept
Asset type: individual 2D Breakout brick texture displayed at 100 by 50 pixels.
Reference image: ice_brick.webp is ONLY a reference for the 2:1 silhouette, beveled rectangular frame and polished game-art rendering. Generate a NEW material and design, no ice or frost.
Composition: a single front-facing orthographic rectangular brick filling the whole landscape image edge to edge, exactly 2:1. No perspective, no surrounding scene, no margins, no text, no letters, no watermark. Broad shapes and high contrast readable at 100x50. Refined stylized material detail, upper-left lighting, bevel around the entire edge.
Primary request: An ordinary destructible terracotta brick. Warm burnt-orange ceramic face, thick beveled orange-red edges, subtly rough baked clay, a few small cracks and chips. One single solid brick, no wall or grid of small bricks, no symbol. Large quiet center, crisp highlights and rich warm shadows.
```

### Accélératrice

```text
Use case: stylized-concept
Asset type: individual 2D Breakout brick texture displayed at 100 by 50 pixels.
Reference image: ice_brick.webp is ONLY a reference for the 2:1 silhouette, beveled rectangular frame and polished game-art rendering. Generate a NEW material and design, no ice or frost.
Composition: a single front-facing orthographic rectangular brick filling the whole landscape image edge to edge, exactly 2:1. No perspective, no surrounding scene, no margins, no text, no letters, no watermark. Broad shapes and high contrast readable at 100x50. Refined stylized material detail, upper-left lighting, bevel around the entire edge.
Primary request: A speed accelerator brick. Golden yellow and amber energy panel, metallic beveled gold frame, a single large luminous white lightning bolt centered on the face, a few horizontal golden speed trails flanking the bolt, energetic orange highlights. Strong readable lightning silhouette, clean graphic composition.
```

### Explosive

```text
Use case: stylized-concept
Asset type: individual 2D Breakout brick texture displayed at 100 by 50 pixels.
Reference image: ice_brick.webp is ONLY a reference for the 2:1 silhouette, beveled rectangular frame and polished game-art rendering. Generate a NEW material and design, no ice or frost.
Composition: a single front-facing orthographic rectangular brick filling the whole landscape image edge to edge, exactly 2:1. No perspective, no surrounding scene, no margins, no text, no letters, no watermark. Broad shapes and high contrast readable at 100x50. Refined stylized material detail, upper-left lighting, bevel around the entire edge.
Primary request: An explosive brick. Deep scarlet red enamel and dark red beveled metal frame. A single large dark charcoal cartoon round bomb pictogram with a short curved fuse and a bright orange spark, centered on a red panel. A few bold yellow-orange warning accents at the outer sides, subtle glowing cracks. Crisp recognizable bomb silhouette, no lettering.
```

### Indestructible

```text
Use case: stylized-concept
Asset type: individual 2D Breakout brick texture displayed at 100 by 50 pixels.
Reference image: ice_brick.webp is ONLY a reference for the 2:1 silhouette, beveled rectangular frame and polished game-art rendering. Generate a NEW material and design, no ice or frost.
Composition: a single front-facing orthographic rectangular brick filling the whole landscape image edge to edge, exactly 2:1. No perspective, no surrounding scene, no margins, no text, no letters, no watermark. Broad shapes and high contrast readable at 100x50. Refined stylized material detail, upper-left lighting, bevel around the entire edge.
Primary request: An indestructible armored brick. Brushed gunmetal steel face with thick silver beveled edges, four round metal rivets near the corners and one prominent raised steel shield emblem in the center. Dark graphite, silver and cool blue reflections. Dense solid unbroken metal, tough and immovable. No cracks, no glowing magic, clear bold shield silhouette.
```

### Duplicatrice

```text
Use case: stylized-concept
Asset type: individual 2D Breakout brick texture displayed at 100 by 50 pixels.
Reference image: ice_brick.webp is ONLY a reference for the 2:1 silhouette, beveled rectangular frame and polished game-art rendering. Generate a NEW material and design, no ice or frost.
Composition: a single front-facing orthographic rectangular brick filling the whole landscape image edge to edge, exactly 2:1. No perspective, no surrounding scene, no margins, no text, no letters, no watermark. Broad shapes and high contrast readable at 100x50. Refined stylized material detail, upper-left lighting, bevel around the entire edge.
Primary request: A ball duplicator brick. Vivid amethyst purple energy face and violet beveled crystal frame. A single clear luminous pictogram centered: one white ball on the left splits via two branching white arrows into two white balls vertically aligned on the right. Three balls total. Minimal bold branching geometry, cyan and pink highlights, quiet violet background for readable white symbol.
```
