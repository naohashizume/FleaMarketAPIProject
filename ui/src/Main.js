import React from "react";
import { Card, CardImg, CardBody, CardText, CardTitle } from "reactstrap";

function Main(props) {
  return (
    <Card style={{ width: "18rem" }}>
      <CardImg
        height={100}
        src="https://www.europarl.europa.eu/resources/library/images/20160609PHT31661/20160609PHT31661_original.jpg"
      />
      <CardBody>
        <CardTitle>Number of Sell Request</CardTitle>
        <CardText>{props.numSellRequest}</CardText>
        <CardTitle>Number of Buy Request</CardTitle>
        <CardText>{props.numBuyRequest}</CardText>
        <CardTitle>First Item for Sell Request</CardTitle>
        <CardText>{props.firstItemSellRequest}</CardText>
        <CardTitle>First Item for Buy Request</CardTitle>
        <CardText>{props.firstItemBuyRequest}</CardText>
        <CardTitle>Last Updated</CardTitle>
        <CardText>{props.dateLastUpdated}</CardText>
      </CardBody>
    </Card>
  );
}

export default Main;
