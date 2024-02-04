import { Owner } from "../services/Board.js";

export default class BugHexagon extends HTMLElement {
    constructor() {
        super();
    }

    connectedCallback() {
        this.addEventListener("click", (e) => {
            const ds = e.currentTarget.dataset;
            console.log("ds", ds);
            if (app.store.board.isAllowed(ds.i)) {
                if (app.store.myTurn) {
                    app.store.board.set(ds.i, Owner.PLAYER);
                    app.store.myTurn = false;
                    this.children[0].classList.add("player");
                } else {
                    app.store.board.set(ds.i, Owner.ENEMY);
                    app.store.myTurn = false;
                    app.store.myTurn = true;
                    this.children[0].classList.add("enemy");
                }
                app.store.board.setIsAllowed(ds.i, false);
            } else {
                alert(`Hexagon ${ds.i} (${ds.x}, ${ds.y}) is not allowed`);
            }
        })

        const inner = document.createElement("div");
        inner.classList.add("inner-hexagon");
        this.append(inner);
    }

    disconnectedCallback() {
        console.log("Custom element removed from page.");
      }
    
    adoptedCallback() {
        console.log("Custom element moved to new page.");
    }

    attributeChangedCallback(name, oldValue, newValue) {
        console.log(`Attribute ${name} has changed from ${oldValue} to ${newValue}.`);
      
    }
}

customElements.define("bug-hexagon", BugHexagon);