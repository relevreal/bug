export default class Board {
    constructor(size) {
        this.size = size;
        this.nRows = 2 * size - 1;
        this.nHexs = nHexsFromBoardSize(size);
        this.board = new Array(this.nHexs).fill(0);
        this.allowed = new Set(Array(this.nHexs).keys());
    }

    get(idx) {
        return this.board[idx];
    }

    set(idx, owner) {
        this.board[idx] = owner;
    }

    isAllowed(idx) {
        return this.allowed.has(parseInt(idx));
    }

    setIsAllowed(idx, allowed) {
        const i = parseInt(idx);
        if (allowed) {
            return this.allowed.add(i);
        }
        return this.allowed.delete(i);
    }

}

function nHexsFromBoardSize(boardSize) {
    let nHexs = 2 * boardSize - 1;
    for (let i = 0; i < boardSize - 1; i++) {
        nHexs += 2 * (boardSize + i);
    }
    return nHexs;
}

export const Owner = {
    NOBODY: 0,
    PLAYER: 1,
    ENEMY: 2,
};

// hold player bugs
// hold enemy bugs