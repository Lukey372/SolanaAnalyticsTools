import React from "react";
import '../cards.css'
const axios = require('axios')
const address = "FQDbLy5PnP511ZTNj4KrTPo2WnKdsciFwGpkRevw69K4"

export default class GetJpeggler extends React.Component {
  state = {
    loading: true,
    txns: []
  };

  async componentDidMount() {
    const { data } = await axios.get("https://api.helius.xyz/v0/addresses/FQDbLy5PnP511ZTNj4KrTPo2WnKdsciFwGpkRevw69K4/nft-events?api-key=4f87c21f-e412-4d7d-9cb9-28424c83508b&until=");
    this.setState({ txns: data, loading: false });
  }

  render() {
    if (this.state.loading) {
      return <div>Loading...</div>;
    }


    return (
      <div>
        {this.state.txns.map(tx => (
            <div key={tx.signature}>
            <div class="card card-3">
              <div class="card__icon"><i class="fas fa-bolt"></i></div>
              <p class="card__exit"><i class="fas fa-times"></i></p>
              <h2 class="card__title">Transaction</h2>
              <p class="card__apply">{tx.description.replace(address, "Jagoe")}</p>

            </div>
          </div>
        ))}
      </div>
    );
  }
}


