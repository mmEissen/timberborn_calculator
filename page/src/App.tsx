import { useEffect, useState } from 'react';
import './App.css';
import { ProductionMenu } from './components/ProductionMenu';
import { ProductionView } from './components/ProductionView';
import { TimberbornContext, Timberborn, createPyodideContext } from './pyodideContext';


function App() {
  const [productionChain, setProductionChain] = useState<Timberborn | null>(null);
  const [faction, setFaction] = useState<string | null>(null);
  const [product, setProduct] = useState<string | null>(null);
  
  useEffect(() => {
    async function set() {
      const productionChain = await createPyodideContext();
      setProductionChain(productionChain);
    }
    set()
  }, [])

  if (productionChain === null) {
    return <div>loading...</div>;
  }


  return (
    <TimberbornContext.Provider value={productionChain}>
      <div className='flex h-screen'>
        <div className='flex-none w-96 h-full bg-fuchsia-100'>
          <ProductionMenu 
            faction={faction}
            onFactionChanged={setFaction}
            product={product}
            onProductChanged={setProduct}
          ></ProductionMenu>
        </div>
        <div className='grow h-full bg-fuchsia-50'>
          <ProductionView
            faction={faction}
            product={product}
          ></ProductionView>
        </div>
      </div>
    </TimberbornContext.Provider>
  );
}

export default App;
