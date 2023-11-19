async function main() {
    let pyodide = await loadPyodide();

    await pyodide.loadPackage("micropip");

    const micropip = pyodide.pyimport("micropip");

    await micropip.install(
        "../dist/production_chain-0.1.0-py3-none-any.whl"
    );

    pyodide.runPython(`
        import production_chain
    `);

    let production_chain = pyodide.globals.get("production_chain");
    d3.select("#graph").graphviz().renderDot(production_chain.dot_graph());
}

main();
