import { createContext } from 'react';

// @ts-ignore
export const TimberbornContext = createContext<Timberborn>(null);

export interface Timberborn {
    getFactions: () => string[]
    getProducts: (faction: string) => string[]
    dotGraph: (faction: string, products: string) => string
}

export async function createPyodideContext() : Promise<Timberborn> {
    // @ts-ignore
    let pyodide = await window.loadPyodide();
    await pyodide.loadPackage("micropip");
    const micropip = pyodide.pyimport("micropip");
    await micropip.install(
        process.env.PUBLIC_URL + "/dist/production_chain-0.1.0-py3-none-any.whl"
    );
    pyodide.runPython(`
        from production_chain import pyodine_interface
    `);
  
    return pyodide.globals.get("pyodine_interface");
}