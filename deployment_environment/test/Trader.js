const {
  time,
  loadFixture,
} = require("@nomicfoundation/hardhat-network-helpers");
const { anyValue } = require("@nomicfoundation/hardhat-chai-matchers/withArgs");
const { expect } = require("chai");

describe("Trader", function () {
  // We define a fixture to reuse the same setup in every test.
  // We use loadFixture to run this setup once, snapshot that state,
  // and reset Hardhat Network to that snapshot in every test.
  async function deployTrader() {
    const univ3router = '0xE592427A0AEce92De3Edee1F18E0157C05861564';
    const weth = '0xc778417E063141139Fce010982780140Aa0cD5Ab';
    const dai = '0x31F42841c2db5173425b5223809CF3A38FEde360';
    const Trader = await hre.ethers.getContractFactory("Trader");
    const trader = await Trader.deploy(univ3router, dai, weth);
  
    await trader.deployed();

    return {trader, weth, dai};
  }

  describe("Deployment", function () {
    it("Should deploy the trader", async function () {
      const {trader, weth, dai} = await deployTrader();

      expect(await trader.getDAI()).to.equal(dai);
      expect(await trader.getWETH9()).to.equal(weth);

    });

})});
