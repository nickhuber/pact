(function() {
    'use strict';
    var characterControllers = angular.module('characterControllers', ['hc.marked']);


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
    });
})();
