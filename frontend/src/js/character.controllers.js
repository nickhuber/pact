(function() {
    'use strict';
    var characterControllers = angular.module('characterControllers', ['hc.marked']);

    var pathfinderTemplate =
        "**XP □**" +
        "\n\n□" +
        "\n\n**Init** □; **Senses** □; **Perception** □" +
        "\n\nDefense" +
        "\n  -------" +
        "\n**AC** □,\ntouch □,\nflat-footed □" +
        "\n\n**Saves** Fort □,\nRef □,\nWill □" +
        "\n\nOffense" +
        "\n  -------" +
        "\n**Speed** □ft." +
        "\n\n**Melee** □" +
        "\n\n**Ranged** □" +
        "\n\n**Special Attacks** □" +
        "\n\nStatistics" +
        "\n  ----------" +
        "\n**Base Atk** □; **CMB** □; **CMD** □" +
        "\n\nSpecial Abilities" +
        "\n  ----------";


    characterControllers.controller('CharacterListCtrl', function ($scope, players, npcs) {
        $scope.players = players;
        $scope.npcs = npcs;
    });


    characterControllers.controller('CharacterDetailCtrl', function ($scope, $location, character) {
        $scope.character = character;
        $scope.errors = {};

        $scope.update = function() {
            $scope.character.$update().then(function(response) {
                $scope.errors = {};
            }).catch(function(response) {
                $scope.errors = response.data;
            });
        };

        $scope.delete = function() {
            $scope.character.$delete().then(function() {
                $location.path('/characters/');
            }).catch(function(response) {
                // TODO: show delete error
            });
        };

        $scope.pathfinderTemplate = function() {
            $scope.character.description = pathfinderTemplate;
        };
    });

    characterControllers.controller('CharacterCreateCtrl', function ($scope, $location, Character) {
        $scope.character = new Character();
        $scope.errors = {};

        $scope.create = function() {
            $scope.character.$save().then(function(newCharacter) {
                $location.path('/characters/' + newCharacter.uuid);
            }).catch(function(errorResponse) {
                $scope.errors = errorResponse.data;
            });
        };

        $scope.pathfinderTemplate = function() {
            $scope.character.description = pathfinderTemplate;
        };
    });

})();
