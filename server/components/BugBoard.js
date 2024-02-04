import Board from "../services/Board.js";

const alpha = Array.from(Array(26)).map((e, i) => i + 97);
const alphabet = alpha.map(x => String.fromCharCode(x));

export default class BugBoard extends HTMLElement {
    constructor() {
        super();

        this.shadow = this.attachShadow({ mode: "open"});

        const styles = document.createElement("style");
        this.shadow.appendChild(styles);

        async function loadCSS() {
          const request = await fetch("/components/BugBoard.css");
          styles.textContent = await request.text();
        }
        loadCSS();
        
    }

    connectedCallback() {
        const boardSize = parseInt(this.getAttribute("size"));

        const sheet = new CSSStyleSheet();
        this.shadow.adoptedStyleSheets = [sheet];

        const resizeObserver = new ResizeObserver(entries => {
            for (let entry of entries) {
                const size = entry.contentBoxSize[0].inlineSize / (2 * boardSize - 1) - 3; 
                console.log("resized entry", size);
                sheet.replaceSync(`:host { --hex-size: ${size}px; }`);
            }
        })
        resizeObserver.observe(this);

        const container = document.createElement("div");
        container.classList.add("container");
        let ii = 0;
        for (const [rowI, rowSize, x] of rowSizeGenerator(boardSize)) {
            const rowDiv = document.createElement("div");
            rowDiv.classList.add("row");
            const rowAlphabet = alphabet.slice(x, x + rowSize);
            for (let i = 0; i < rowSize; i++) {
                const hexagon = document.createElement("bug-hexagon");
                hexagon.setAttribute("data-x", rowI);
                hexagon.setAttribute("data-y", rowAlphabet[i]);
                hexagon.setAttribute("data-i", ii);
                hexagon.classList.add("allowed");
                rowDiv.appendChild(hexagon);
                console.log(`hex: (${rowI}, ${rowAlphabet[i]})`);
                ii += 1;
            }
            container.appendChild(rowDiv);
        }
        this.shadow.appendChild(container);
        app.board = new Board(boardSize);
    }
}

function* rowSizeGenerator(boardSize) {
    const nRows = 2 * boardSize - 1;
    const middleRow = boardSize;
    let rowSize = boardSize;
    let x = boardSize - 1;
    yield [1, rowSize, x];
    for (let rowI = 1; rowI < nRows; rowI++) {
        if (rowI < middleRow) {
            rowSize += 1;
            x -= 1;
        } else {
            rowSize -= 1;
        }
        yield [rowI + 1, rowSize, x];
    }
}

customElements.define("bug-board", BugBoard);