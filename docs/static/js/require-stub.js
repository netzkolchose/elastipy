
function require(names, func) {

    if (names[0] === "plotly") {
        func(Plotly);
        return;
    }

    throw `packages '${names}' not available`
}
