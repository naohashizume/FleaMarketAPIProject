import React, { useState, useEffect } from "react";
import Main from "./Main";
import axios from "axios";
import "./App.css";

function App() {
  const [data, SetData] = useState("data");
  const [numBuyRequest, SetNumBuyRequset] = useState(0);
  const [numSellRequest, SetNumSellRequset] = useState(0);
  const [dateLastUpdated, SetDateLastUpdated] = useState("default");
  const [firstItemBuyRequest, SetFirstItemBuyRequest] = useState("default");
  const [firstItemSellRequest, SetFirstItemSellRequest] = useState("default");

  let URL1 =
    "http://a01022269-lab8.westus2.cloudapp.azure.com:8100/sell_request?startDate=2016-01-01T11:55:01&endDate=2023-01-31T11:56:01";
  let URL2 =
    "http://a01022269-lab8.westus2.cloudapp.azure.com:8110/sell_request/first";
  let URL3 =
    "http://a01022269-lab8.westus2.cloudapp.azure.com:8110/buy_request/first";

  const fetchURL = url => axios.get(url);

  const promiseArray = [URL1, URL2, URL3].map(fetchURL);

  const getAllData = () => {
    Promise.all(promiseArray)
      .then(arr => {
        SetData(arr);
        SetNumBuyRequset(data[0].data.num_buy_request);
        SetNumSellRequset(data[0].data.num_sell_request);
        SetDateLastUpdated(data[0].data.timestamp);
        SetFirstItemSellRequest(data[1].data.item_name);
        SetFirstItemBuyRequest(data[2].data.item_name);
      })
      .catch(err => {
        console.log(err);
      });
  };

  useEffect(() => {
    console.log("This will run after 2 second!");
    setTimeout(getAllData, 2000);
  }, [data]);

  return (
    <div className="App">
      <Main
        numSellRequest={numBuyRequest}
        numBuyRequest={numSellRequest}
        firstItemSellRequest={firstItemSellRequest}
        firstItemBuyRequest={firstItemBuyRequest}
        dateLastUpdated={dateLastUpdated}
      />
    </div>
  );
}

export default App;
