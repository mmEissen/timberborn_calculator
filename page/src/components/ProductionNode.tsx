import { Handle, Position } from "reactflow";


interface Props {
    id: string;
    data: Data;
}

interface Data {
    facilityName: string;
    recipeName: string;
    numberFacilities: Fraction;
    resources: string[];
    products: string[];
}

interface Fraction {
    integer: number;
    numerator: number;
    denominator: number;
}

interface Handle {
    id: string;
    name: string;
}

export function ProductionNode(props: Props) {
    return (
        <div className="w-64">
            <div className="flex bg-fuchsia-300">
                <div className="flex-grow">
                    <div className="flex-none">
                        {props.data.facilityName}
                    </div>
                    <div className="flex-none">
                        {props.data.recipeName}
                    </div>
                </div>
                <div className="flex-none w-16 h-full bg-fuchsia-200 text-center align-middle text-xl">
                    {props.data.numberFacilities.integer}
                    {
                        props.data.numberFacilities.numerator > 0 
                        ? <>
                            <sup>{props.data.numberFacilities.numerator}</sup>
                            &frasl;
                            <sub>{props.data.numberFacilities.denominator}</sub>
                        </>
                        : <></>
                    }
                    
                </div>
            </div>
            <div className="flex-none grid grid-cols-2">
                <Resources resources={props.data.resources}></Resources>
                <Products products={props.data.products}></Products>
            </div>
        </div>
    );
}

interface ResourcesProps {
    resources: string[]
}

function Resources(props: ResourcesProps) {
    return <div className='flex-none grid grid-cols-1 content-center bg-fuchsia-100'>
        {
            props.resources.map(resource => {
                return (
                    <div style={{ position: "relative" }}>
                        {resource}
                        <Handle type="target" id={resource} position={Position.Left}></Handle>
                    </div>
                )
            })
        }
    </div>
}

interface ProductsProps {
    products: string[]
}

function Products(props: ProductsProps) {
    return <div className='flex-none grid grid-cols-1 content-center bg-fuchsia-200'>
        {
            props.products.map(product => {
                return (
                    <div style={{ position: "relative" }}>
                        {product}
                        <Handle type="source" id={product} position={Position.Right}></Handle>
                    </div>
                )
            })
        }
    </div>
}
