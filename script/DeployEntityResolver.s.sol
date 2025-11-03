// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.26;

import {Script, console} from "forge-std/Script.sol";
import {EntitiesResolver} from "../resolvers/EntitiesResolver.sol";
import {EAS} from "eas-contracts/EAS.sol";
import {TransparentUpgradeableProxy} from "@openzeppelin/contracts/proxy/transparent/TransparentUpgradeableProxy.sol";

contract DeployEntityResolverScript is Script {
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

        // Deploy ProjectAttesterResolver contract
        EntitiesResolver implementation = new EntitiesResolver();

        TransparentUpgradeableProxy proxy = new TransparentUpgradeableProxy(
            address(implementation),
            deployer,
            abi.encodeWithSelector(
                EntitiesResolver.initialize.selector,
                eas,
                deployer,
                initialAttesters
            )
        );

        vm.stopBroadcast();

        console.log("Deployed EntityResolver at address:", address(proxy));
    }
}
