var combatTrackerServices = angular.module('combatTrackerServices', ['ngResource']);

combatTrackerServices.factory('Player', ['$resource', function($resource) {
    return $resource('api/players/:playerID', {playerID: '@id'});
}]);

combatTrackerServices.factory('NPC', ['$resource', function($resource) {
    return $resource('api/npc_templates/:NPCID', {NPCID: '@id'});
}]);
