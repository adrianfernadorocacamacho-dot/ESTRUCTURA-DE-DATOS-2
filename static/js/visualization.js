// Minimal, clear canvas rendering for BST, AVL, and M-vías
// Fetch tree data and render on load

(function () {
  const CANVAS_IDS = {
    bst: 'canvas-bst',
    avl: 'canvas-avl',
    mvias: 'canvas-mvias',
  };

  function onReady(fn) {
    if (document.readyState !== 'loading') {
      fn();
    } else {
      document.addEventListener('DOMContentLoaded', fn);
    }
  }

  function getCtx(id) {
    const canvas = document.getElementById(id);
    return canvas ? canvas.getContext('2d') : null;
  }

  function clearCanvas(ctx) {
    if (!ctx) return;
    const { width, height } = ctx.canvas;
    ctx.clearRect(0, 0, width, height);
    // background
    ctx.fillStyle = '#0b1220';
    ctx.fillRect(0, 0, width, height);
  }

  // Layout helpers for binary trees
  function computePositionsBinary(root, depth = 0, xMin = 40, xMax = 560, levelHeight = 70, positions = []) {
    if (!root) return positions;
    const x = (xMin + xMax) / 2;
    const y = 40 + depth * levelHeight;
    positions.push({ node: root, x, y });
    if (root.left) computePositionsBinary(root.left, depth + 1, xMin, x - 30, levelHeight, positions);
    if (root.right) computePositionsBinary(root.right, depth + 1, x + 30, xMax, levelHeight, positions);
    return positions;
  }

  // Layout for M-vías: place keys as a box and children spread beneath
  function computePositionsMVias(root, originX = 300, originY = 40, levelHeight = 90, positions = []) {
    if (!root) return positions;
    // compute subtree widths to space children
    const subtreeWidth = getSubtreeWidthMVias(root);
    const x = originX;
    const y = originY;
    positions.push({ node: root, x, y, width: subtreeWidth });
    const children = root.children || [];
    let cursor = x - subtreeWidth / 2;
    const gap = 20;
    const childY = y + levelHeight;
    for (let i = 0; i < children.length; i++) {
      const child = children[i];
      if (!child) continue;
      const cw = getSubtreeWidthMVias(child);
      const childX = cursor + cw / 2;
      computePositionsMVias(child, childX, childY, levelHeight, positions);
      cursor += cw + gap;
    }
    return positions;
  }

  function getSubtreeWidthMVias(node) {
    if (!node) return 0;
    const baseWidth = Math.max(60, (node.keys?.length || 0) * 24 + 20);
    const children = node.children || [];
    const childWidths = children.map(getSubtreeWidthMVias).filter(w => w > 0);
    if (childWidths.length === 0) return baseWidth;
    const sum = childWidths.reduce((a, b) => a + b, 0) + Math.max(0, childWidths.length - 1) * 20;
    return Math.max(baseWidth, sum);
  }

  function drawEdge(ctx, x1, y1, x2, y2) {
    ctx.strokeStyle = '#8da2fb';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(x1, y1);
    ctx.lineTo(x2, y2);
    ctx.stroke();
  }

  function drawNodeCircle(ctx, x, y, text) {
    const r = 16;
    ctx.fillStyle = '#1f2a44';
    ctx.strokeStyle = '#a0aec0';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.arc(x, y, r, 0, 2 * Math.PI);
    ctx.fill();
    ctx.stroke();
    ctx.fillStyle = '#e2e8f0';
    ctx.font = '12px Segoe UI, sans-serif';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(String(text), x, y);
  }

  function drawNodeBox(ctx, x, y, keys) {
    const text = (keys || []).join(' | ');
    const width = Math.max(60, text.length * 7 + 20);
    const height = 26;
    const rx = 8;
    const left = x - width / 2;
    const top = y - height / 2;
    // box
    ctx.fillStyle = '#1f2a44';
    ctx.strokeStyle = '#a0aec0';
    ctx.lineWidth = 2;
    roundRect(ctx, left, top, width, height, rx);
    ctx.fill();
    ctx.stroke();
    // text
    ctx.fillStyle = '#e2e8f0';
    ctx.font = '12px Segoe UI, sans-serif';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(text || '∅', x, y);
  }

  function roundRect(ctx, x, y, w, h, r) {
    ctx.beginPath();
    ctx.moveTo(x + r, y);
    ctx.arcTo(x + w, y, x + w, y + h, r);
    ctx.arcTo(x + w, y + h, x, y + h, r);
    ctx.arcTo(x, y + h, x, y, r);
    ctx.arcTo(x, y, x + w, y, r);
    ctx.closePath();
  }

  function drawBinary(ctx, root) {
    clearCanvas(ctx);
    if (!root) return;
    const positions = computePositionsBinary(root);
    // edges
    for (const p of positions) {
      if (p.node.left) {
        const child = positions.find(q => q.node === p.node.left);
        if (child) drawEdge(ctx, p.x, p.y + 16, child.x, child.y - 16);
      }
      if (p.node.right) {
        const child = positions.find(q => q.node === p.node.right);
        if (child) drawEdge(ctx, p.x, p.y + 16, child.x, child.y - 16);
      }
    }
    // nodes
    for (const p of positions) {
      drawNodeCircle(ctx, p.x, p.y, p.node.value);
    }
  }

  function drawMVias(ctx, root) {
    clearCanvas(ctx);
    if (!root) return;
    const positions = computePositionsMVias(root);
    // edges: connect parent box bottom to child box top
    for (const p of positions) {
      const parent = p;
      const children = (p.node.children || []).filter(Boolean);
      for (const child of children) {
        const pc = positions.find(q => q.node === child);
        if (pc) drawEdge(ctx, parent.x, parent.y + 14, pc.x, pc.y - 14);
      }
    }
    // nodes
    for (const p of positions) {
      drawNodeBox(ctx, p.x, p.y, p.node.keys);
    }
  }

  async function fetchAndRender() {
    try {
      const res = await fetch('/api/tree_data');
      if (!res.ok) return;
      const data = await res.json();
      drawBinary(getCtx(CANVAS_IDS.bst), data.bst);
      drawBinary(getCtx(CANVAS_IDS.avl), data.avl);
      drawMVias(getCtx(CANVAS_IDS.mvias), data.mvias);
    } catch (e) {
      // ignore
    }
  }

  onReady(() => {
    fetchAndRender();
    // Re-render on any form submit completion via simple polling
    const observer = new MutationObserver(() => fetchAndRender());
    observer.observe(document.body, { childList: true, subtree: true });
  });
})();


