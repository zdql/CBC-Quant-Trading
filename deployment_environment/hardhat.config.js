require("@nomicfoundation/hardhat-toolbox");
require('dotenv').config()

// a new App in its dashboard, and replace "KEY" with its key
const ROPSTEN_API_KEY = process.env.ROPSTEN_API_KEY;

// Replace this private key with your Goerli account private key
// To export your private key from Metamask, open Metamask and
// go to Account Details > Export Private Key
// Beware: NEVER put real Ether into testing accounts
const PRIVATE_KEY = process.env.ROPSTEN_PRIVATE_KEY;



/** @type import('hardhat/config').HardhatUserConfig */
module.exports = {
  solidity:     {  compilers: [
    {
      version: "0.7.6"
    },
    {
      version: "0.8.0"
    }
  ],
},
networks: {
  ropsten: {
    url: `${ROPSTEN_API_KEY}`,
    accounts: [PRIVATE_KEY]
  }
}
};
