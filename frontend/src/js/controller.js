var combatTrackerControllers = angular.module('combatTrackerControllers', []);

// Character controllers
combatTrackerControllers.controller('CharacterListCtrl', ['$scope', 'Character', 
    function ($scope, Character) {
        $scope.characters = Character.query();
    }
]);

combatTrackerControllers.controller('CharacterDetailCtrl', ['$scope', '$location', '$routeParams', 'Character', 
    function ($scope, $location, $routeParams, Character) {
        $scope.character = Character.get($routeParams);
        $scope.delete = function() {
            $scope.character.$delete({}, function() {
                $location.path('/characters/');
            }, function(response) {
                // TODO: show error
            });
        };
    }
]);

combatTrackerControllers.controller('CharacterCreateCtrl', ['$scope', '$location', 'Character', 
    function ($scope, $location, Character) {
        $scope.character = new Character();
        $scope.errors = {};
        $scope.create = function() {
            $scope.character.$save(
                function(newCharacter) {
                    $location.path('/characters/' + newCharacter['id']);
                },
                function(errorResponse) {
                    $scope.errors = errorResponse.data;
                }
            );
        };
    }
]);

// Encounter controllers
combatTrackerControllers.controller('EncounterListCtrl', ['$scope', 'Encounter', 
    function($scope, Encounter) {
        $scope.encounters = Encounter.query();
    }
]);

combatTrackerControllers.controller('EncounterDetailCtrl', ['$scope', '$location', '$routeParams', 'Encounter', 
    function ($scope, $location, $routeParams, Encounter) {
        $scope.encounter = Encounter.get($routeParams);
        $scope.delete = function() {
            $scope.encounter.$delete({}, function() {
                $location.path('/encounters/');
            }, function(response) {
                // TODO: show error
            });
        };
    }
]);

combatTrackerControllers.controller('EncounterCreateCtrl', ['$scope', '$location', 'Encounter', 
    function ($scope, $location, Encounter) {
        $scope.encounter = new Encounter();
        $scope.create = function() {
            $scope.encounter.$save(function(newEncounter) {
                $location.path('/encounters/' + newEncounter['id']);
            },
            function(response) {
                // TODO: show these errors
            });
        };
    }
]);


// Misc controllers
combatTrackerControllers.controller('NavigationCtrl', ['$scope', '$http', '$location', 
    function ($scope, $http, $location)  { 
        $scope.isActive = function (viewLocation) {
            return $location.$$path === viewLocation;
        };
        $scope.rollQuery = '';
        $scope.rollResult = '';
        $scope.rollDice = function() { 
            $http.post(
                '/api/roll',
                {query: $scope.rollQuery}
            )
            .success(function(results) {
                console.log(results);
                $scope.rollResult = results['total'];
            });
        };
    }
]);
