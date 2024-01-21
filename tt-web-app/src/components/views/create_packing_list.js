import React from "react";
import {Button, Card, CardGroup, Container, Form, Image, Input, Search} from "semantic-ui-react";
import product_manifest from "./products_manifest.json";

function ProductCard({product}) {
    const {image, title} = product;
    let [quantity, setQuantity] = React.useState(1);
    console.log(product)

    function getWeight(product){
        let totalWeight = 0;
        let count = 0
        product.weights.forEach(weight => {
            let value = weight.value.split(" ")[0];
            if(value.includes("kg")){
                totalWeight += parseFloat(value.replace("kg", "")) * 1000
                count += 1;
            } else if(value.includes("g")){
                totalWeight += parseFloat(value.replace("g", ""))
                count += 1;
            } else {
                console.log(`Unknown weight unit ${weight}`)
            }
        })
        if(count === 0){
            return "Unknown"
        }
        return Math.round(totalWeight / count);
    }

    const weight = getWeight(product);
    return <Card>
        <Card.Content>
            <Card.Header>{title}</Card.Header>
            <Card.Meta>
                {weight}g X
                <Input
                    type={"number"}
                    value={quantity}
                    style={{
                        width: "55px",
                        marginLeft: "5px",
                        marginRight: "5px",
                    }}
                    onChange={(e) => {
                        setQuantity(e.target.value)
                    }}
                />
                = {weight * quantity}g
            </Card.Meta>
        </Card.Content>
        <div style={{
            width:"200px",
            height:"200px",
            overflow:"hidden",
        }} >
            <Image centered src={image} style={{
                maxWidth:"100%",
                maxHeight:"100%",
                verticalAlign:"middle",
            }}/>
        </div>
    </Card>
}

function CreatePackingList() {
    let [name, setName] = React.useState("");
    let [searchText, setSearchText] = React.useState("");
    let [results, setResults] = React.useState([]);
    let [products, setProducts] = React.useState([]);
    function onSave(){

    }

    function updateSearchResults(value){
        let results = [];
        product_manifest.forEach(product => {
            if(results.length >= 5){
                return;
            }
            const title = product.title.toLowerCase();
            const words = value.split(" ");
            let foundWords = []
            words.forEach(word => {
                foundWords.push(title.includes(word.toLowerCase()));
            })
            const show = foundWords.length > 0 && !foundWords.includes(false)
            if(show){
                results.push({
                    title: product.title,
                    image: product.image,
                    weights: product.weights,
                })
            }
        });
        setResults(results);
    }

    function onSearchChange(e){
        setSearchText(e.target.value)
        updateSearchResults(e.target.value);
    }

    function onResultSelect(e, {result}){
        const newProducts = [...products];
        newProducts.push(result);
        setProducts(newProducts);
        setSearchText("");
    }

    return <Container style={{paddingTop:"15px"}}>
        <Form>
            <Form.Field>
                <label>Name</label>
                <Input
                    value={name}
                    placeholder="Name"
                    onChange={(e) => {
                        setName(e.target.value)
                    }}
                />
            </Form.Field>

            <Search
                placeholder="Search for items to add"
                loading={false}
                onResultSelect={onResultSelect.bind(this)}
                onSearchChange={onSearchChange.bind(this)}
                results={results}
                value={searchText}
            />
            <br/>

            <CardGroup stackable itemsPerRow={5}>
                {products.map(product => { return <ProductCard key={product.title} product={product} /> })}
            </CardGroup>
            <br/>

            <Button floated="right" content="Save" onClick={onSave.bind(this)}/>
            <br/>
            <br/>

        </Form>
    </Container>;
}

export default CreatePackingList;