import Store from "../../services/Store.js";
import Board from "../../services/Board.js";

// Link Web Components
import BugHexagon from "../../components/BugHexagon.js";
import BugBoard from "../../components/BugBoard.js";

window.app = {};
app.store = Store;

window.addEventListener("DOMContentLoaded", async () => {
    const body = document.querySelector("body");
    const board = document.createElement("bug-board");
    const boardSize = 6;
    board.setAttribute("size", boardSize);
    app.store.board = new Board(boardSize);
    app.store.myTurn = true;
    body.appendChild(board);
});