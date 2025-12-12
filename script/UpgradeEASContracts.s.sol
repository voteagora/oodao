// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.26;

import {Script, console} from "forge-std/Script.sol";
import {EntitiesResolver} from "../resolvers/EntitiesResolver.sol";
import {VotesResolver} from "../resolvers/VotesResolver.sol";
import {EAS} from "eas-contracts/EAS.sol";
import {ITransparentUpgradeableProxy, TransparentUpgradeableProxy} from "@openzeppelin/contracts/proxy/transparent/TransparentUpgradeableProxy.sol";
import {ProxyAdmin} from "@openzeppelin/contracts/proxy/transparent/ProxyAdmin.sol";

contract UpgradeEASContracts is Script {
    function run() external {
        vm.startBroadcast();

        // Read caller information.
        (, address deployer,) = vm.readCallers();

        address[] memory initialAttesters = new address[](2);
        initialAttesters[0] = deployer;
        initialAttesters[1] = 0x0FD3Cb37718A60293013EED17aC1c78a9b4af1C4;

        // Read EAS contract address from environment variable
        address easAddress = vm.envAddress("EAS_CONTRACT");
        address proxyAdminAddress = vm.envAddress("PROXY_ADMIN");
        address proxy = vm.envAddress("PROXY_CONTRACT");
        uint8 path = uint8(vm.envUint("UPGRADE_PATH"));

        bytes memory reinitialize;
        address implementation;

        EAS eas = EAS(easAddress);
        ProxyAdmin proxyAdmin = ProxyAdmin(proxyAdminAddress);

        if (path == 1) {
            implementation = address(new VotesResolver());
            reinitialize = abi.encodeWithSelector(VotesResolver.initialize.selector, eas, deployer);
        }

        else {
            implementation = address(new EntitiesResolver());
            reinitialize = abi.encodeWithSelector(EntitiesResolver.initialize.selector, eas, deployer, initialAttesters);
        }

        assert(deployer == proxyAdmin.owner());
        proxyAdmin.upgradeAndCall(ITransparentUpgradeableProxy(proxy), implementation, reinitialize);

        vm.stopBroadcast();

        console.log("Upgraded contract at:", address(proxy));
        console.log("With implementation at address:", address(implementation));
    }
}

