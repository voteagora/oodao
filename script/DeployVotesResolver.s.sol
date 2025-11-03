// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.26;

import {Script, console} from "forge-std/Script.sol";
import {VotesResolver} from "../resolvers/VotesResolver.sol";
import {EAS} from "eas-contracts/EAS.sol";
import {TransparentUpgradeableProxy} from "@openzeppelin/contracts/proxy/transparent/TransparentUpgradeableProxy.sol";

contract DeployVotesResolverScript is Script {
    function run() external {

        vm.startBroadcast();

        // Read caller information.
        (, address deployer,) = vm.readCallers();

        address[] memory initialAttesters = new address[](2);
        initialAttesters[0] = deployer;
        initialAttesters[1] = 0x0FD3Cb37718A60293013EED17aC1c78a9b4af1C4;

        // Read EAS contract address from environment variable
        address easAddress = vm.envAddress("EAS_CONTRACT");
        EAS eas = EAS(easAddress);

        // Deploy VotesResolver contract
        VotesResolver implementation = new VotesResolver();

        TransparentUpgradeableProxy proxy = new TransparentUpgradeableProxy(
            address(implementation),
            deployer,
            abi.encodeWithSelector(
                VotesResolver.initialize.selector,
                eas,
                deployer
            )
        );

        vm.stopBroadcast();

        console.log("Deployed VotesResolver at address:", address(proxy));
    }
}
