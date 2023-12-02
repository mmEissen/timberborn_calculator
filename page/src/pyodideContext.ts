import { createContext } from 'react';

// @ts-ignore
export const TimberbornContext = createContext<Timberborn>(null);


interface Node {
    id: string;
    facilityName: string;
    recipeName: string;
    resourceNames: string[];
    productNames: string[];
    numberFacilities: Fraction;
}

interface Fraction {
    integer: number;
    numerator: number;
    denominator: number;
}

interface Edge {
    id: string;
    source: string;
    target: string;
    resource: string;
}

export interface Timberborn {
    getFactions: () => string[];
    getProducts: (faction: string) => string[];
    dotGraph: (faction: string, products: string) => string;
    graph: (faction: string, products: string) => [Node[], Edge[]];
}


function funcToJs(pyFunc: any) {
    return (...args : any[]) => pyFunc(...args).toJs({dict_converter : Object.fromEntries})
}

function toInterface(pyObject: any) : Timberborn {
    return {
        getFactions: funcToJs(pyObject.getFactions),
        getProducts: funcToJs(pyObject.getProducts),
        dotGraph: funcToJs(pyObject.dotGraph),
        graph: funcToJs(pyObject.graph)
    };
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
  
    return toInterface(pyodide.globals.get("pyodine_interface"));
}