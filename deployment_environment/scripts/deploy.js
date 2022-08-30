// We require the Hardhat Runtime Environment explicitly here. This is optional
// but useful for running the script in a standalone fashion through `node <script>`.
//
// You can also run a script with `npx hardhat run <script>`. If you do that, Hardhat
// will compile your contracts, add the Hardhat Runtime Environment's members to the
// global scope, and execute the script.
const hre = require("hardhat");

async function main() {
  const univ3router = '0xE592427A0AEce92De3Edee1F18E0157C05861564';
  const weth = '0xc778417E063141139Fce010982780140Aa0cD5Ab';
  const dai = '0x31F42841c2db5173425b5223809CF3A38FEde360';
  const fee = 3000;
  const Trader = await hre.ethers.getContractFactory("Trader");
  const trader = await Trader.deploy(univ3router, weth, dai);

  await trader.deployed();

  console.log(
    `Deployed UNIv3 Trader for ${weth} and ${dai} with fee: ${fee} deployed to ${trader.address}`
  );
}

// We recommend this pattern to be able to use async/await everywhere
// and properly handle errors.
main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
