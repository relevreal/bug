const Store = {
    myTurn: null,
    board: null,
};

const proxiedStore = new Proxy(Store, {
    set(target, property, value) {
        target[property] = value;
        if (property == "myTurn") {
            window.dispatchEvent(new Event("appmyturnchange"));
        }
        // else if (property == "boardSize") {
        //     window.dispatchEvent(new Event("appboardsizechange"));
        //     Store.board = [];
        // }
        else if (property == "board") {
            window.dispatchEvent(new Event("appboardchange"));
        }
        return true;
    }
})

export default proxiedStore;