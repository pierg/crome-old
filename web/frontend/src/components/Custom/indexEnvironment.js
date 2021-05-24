function _n(val, def) {
  return (typeof val === 'number') ? val : def;
}

const floor = Math.floor;

function Node(x, y, backgroundColor) {
  this.x = x;
  this.y = y;
  this.backgroundColor = backgroundColor || null;
  this.blocked = false;
}

Node.prototype = {
  toString: function() {
    return "<node x=" + this.x + " y=" + this.y + " blocked=" + this.blocked + ">";
  }
}

function GridWorld(canvas, width, height, options) {

  options = options || {};

  this.canvas  = canvas;
  this.ctx     = canvas.getContext('2d');
  this.width   = floor(width) * 2 ;
  this.height  = floor(height) * 2 ;

  let padding = options.padding;

  if (typeof padding === 'undefined') {
    padding = 0;
  }

  if (typeof padding === 'number') {
    this.padding = {
      top     : padding,
      right   : padding,
      bottom  : padding,
      left    : padding
    };
  } else {
    this.padding = padding;
  }

  this.cellSize = _n(options.cellSize, 25);
  this.cellSizeWall = _n(options.cellSize, 5);
  this.cellSpacing = _n(options.cellSpacing, 2);
  this.drawBorder = !!options.drawBorder;
  this.borderColor = options.borderColor || 'lightgrey';
  this.backgroundColor = options.backgroundColor || 'white';

  if (options.resizeCanvas) {
    let cw = this.padding.left + this.padding.right,
        ch = this.padding.top + this.padding.bottom;
    cw += ((this.width) * (this.cellSize +  this.cellSizeWall + this.cellSpacing));
    ch += ((this.height) * (this.cellSize + this.cellSizeWall + this.cellSpacing)) -  2 * this.cellSize;

    if (this.drawBorder) {
      cw += (this.cellSpacing * 2);
      ch += (this.cellSpacing * 2);
    }
    this.canvas.width = cw;
    this.canvas.height = ch;
  }

  this.nodes = [];
  console.log(this.width);
  console.log(this.height);
  for (let j = 0; j < this.height + 1; ++j) {
    for (let i = 0; i < this.width + 1; ++i) {
      this.nodes.push(new Node( i,j, null));
    }
  }
  console.log("node : " +this.nodes.length);

  //
  // Event handling
  // TODO: support dragging

  const self = this;

  this.onclick = options.onclick;

  function p2n(x, y) {

    x -= self.padding.left;
    y -= self.padding.top;

    if (self.drawBorder) {
      x -= (self.cellSpacing * 2);
      y -= (self.cellSpacing * 2);
    }
    console.log("y : " + y);
    let a = 2 * self.cellSpacing + 2 * self.cellSizeWall;
    let b = a;
    const tabX = [a];
    const tabY = [b];

    for (let i = 0; i < self.width; i+=2) {
      a += 2 * self.cellSize;
      tabX.push(a);
      b += 2 * self.cellSize;
      tabY.push(b);

      a += 2 * self.cellSizeWall + self.cellSpacing;
      tabX.push(a);
      b += 2 * self.cellSizeWall + self.cellSpacing;
      tabY.push(b);
      a += self.cellSpacing;
      b += self.cellSpacing;
    }
    let indexX = 0;
    if (x > tabX[0]) {
      indexX = 1;
    }
    while (x >= tabX[indexX] ) {
      indexX++;
    }
    let indexY = 0;
    if (y > tabY[0]) {
      indexY = 1;
    }
    while (y >= tabY[indexY] ) {
      indexY++;
    }

    if (indexX >= 0 && indexX < self.width + 3 * self.cellSizeWall && indexY >= 0 && indexY < self.height + 3 * self.cellSizeWall) {
      return self.nodes[(indexY * (self.width + 1)) + indexX];
    }
    else {
      return null;
    }
  }
  let start =[];
  let end =[];

  canvas.addEventListener('click', function(evt) {

    if (!self.onclick)
      return;

    const node = p2n(evt.offsetX, evt.offsetY);

    if (node) {
      if (node.x % 2 === 1 && node.y % 2 === 1) {
        if (start.length === 0) {
          start.push(node.x);
          start.push(node.y);
          self.onclick(node, start, end);

        } else {
          end.push(node.x);
          end.push(node.y);
          self.onclick(node, start, end);
          start = [];
          end = [];
        }
      }
      else {
        self.onclick(node, start, end);
      }
    }

  });

}

GridWorld.prototype = {
  draw: function() {

    let csz = this.cellSize,
        csz2 = this.cellSizeWall,
        csp = this.cellSpacing,
        ctx = this.ctx,
        ix = 0;

    const bAdj = this.drawBorder ? this.cellSpacing : -this.cellSpacing,
        cAdj = this.drawBorder ? this.cellSpacing : 0;

    ctx.save();
    ctx.fillStyle = this.borderColor;
    ctx.fillRect(this.padding.left,
        this.padding.top,
        (( csz + csz2 + csp) * this.width) + 2 *csz2 + 2 * csp + bAdj,
        ((csz + csz2 + csp) * this.height) + 2 *csz2 + 2 * csp + bAdj);

    let cy = this.padding.top + cAdj;
    for (let j = 0; j < this.height + 1; ++j) {
      let cx = this.padding.left + cAdj;
      for (let i = 0; i < this.width + 1; ++i) {
        const n = this.nodes[ix++];
        ctx.fillStyle = n.backgroundColor || this.backgroundColor;
        if ( j % 2 === 1 ) {
          if (i % 2 === 1) {
            ctx.fillRect(cx, cy, 2 * csz, 2 * csz);
            cx += 2 * csz + csp;
          }
          else  {
            ctx.fillRect(cx, cy,2 * csz2, 2 * csz);
            cx += 2 * csz2 + csp;
          }
        }
        else {
          if (i % 2 === 1) {
            ctx.fillRect(cx, cy, 2 * csz, 2 * csz2);
            cx += 2 * csz + csp;
          }
          else  {
            ctx.fillRect(cx, cy, 2 * csz2, 2 * csz2);
            cx += 2 * csz2 + csp;
          }

        }
      }
      if (j % 2 === 1) {
        cy += 2 * csz + csp;
      }
      else {
        cy += 2 * csz2 + csp;
      }
    }

    ctx.restore();

  },

  get: function(x, y) {
    return this.nodes[(y * (this.width + 1)) + x];
  },

  getBackgroundColor: function(x, y) {
    return this.nodes[(y *  (this.width + 1)) + x].backgroundColor;
  },

  setBackgroundColor: function(x, y, color) {
    this.nodes[(y *  (this.width + 1)) + x].backgroundColor = color;
  },

  isBlocked: function(x, y) {
    return this.nodes[(y *  (this.width + 1)) + x].blocked;
  },

  setBlocked: function(x, y, blocked) {
    this.nodes[(y *  (this.width + 1)) + x].blocked = !!blocked;
  },

  setAttribute: function(x, y, key, value) {
    this.nodes[(y * (this.width + 1)) + x][key] = value;
  },

  eachNeighbour: function(x, y, callback) {
    return this.eachNodeNeighbour(this.nodes[(y *  (this.width + 1)) + x], callback);
  },

  eachNodeNeighbour: function(node, callback) {

    let x = node.x,
        y = node.y,
        w = this.width,
        h = this.height,
        ns = this.nodes,
        ix = (y * w) + x,
        nix = 0;

    if (x > 0   && !ns[ix-1].blocked) callback(ns[ix-1], nix++);
    if (x < w-1 && !ns[ix+1].blocked) callback(ns[ix+1], nix++);
    if (y > 0   && !ns[ix-w].blocked) callback(ns[ix-w], nix++);
    if (y < h-1 && !ns[ix+w].blocked) callback(ns[ix+w], nix++);

  },

  eachNode: function(callback) {
    this.nodes.forEach(callback);
  }

};


export default GridWorld;
