var combatTrackerControllers = angular.module('combatTrackerControllers', []);

// Player controllers
combatTrackerControllers.controller('PlayerListCtrl', ['$scope', 'Player', 
    function ($scope, Player) {
        $scope.players = Player.query();
    }
]);

combatTrackerControllers.controller('PlayerDetailCtrl', ['$scope', '$routeParams', 'Player', 
    function ($scope, $routeParams, Player) {
        $scope.player = Player.get($routeParams);
        $scope.delete = function() {
            $scope.player.$delete({}, function() {
                $location.path('/players/');
            }, function(response) {
                // TODO: show error
            });
        };
    }
]);

combatTrackerControllers.controller('PlayerAddCtrl', ['$scope', '$location', 'Player', 
    function ($scope, $location, Player) {
        $scope.player = new Player();
        $scope.addPlayer = function() {
            $scope.player.$save(function(newPlayer) {
                $location.path('/players/' + newPlayer['id']);
            },
            function(response) {
                // TODO: show these errors
            });
        };
    }
]);

// NPC controllers
combatTrackerControllers.controller('NPCListCtrl', ['$scope', 'NPC', 
    function ($scope, NPC) {
        $scope.npcs = NPC.query();
    }
]);

combatTrackerControllers.controller('NPCDetailCtrl', ['$scope', '$location', '$routeParams', 'NPC', 
    function ($scope, $location, $routeParams, NPC) {
        $scope.npc = NPC.get($routeParams);
        $scope.delete = function() {
            $scope.npc.$delete({}, function() {
                $location.path('/npcs/');
            }, function(response) {
                // TODO: show error
            });
        };
    }
]);

combatTrackerControllers.controller('NPCAddCtrl', ['$scope', '$location', 'NPC', 
    function ($scope, $location, NPC) {
        $scope.npc = new NPC();
        $scope.addNPC = function() {
            $scope.npc.$save(function(newNPC) {
                $location.path('/npcs/' + newNPC['id']);
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
