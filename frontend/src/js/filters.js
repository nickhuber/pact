var combatTrackerFilters = angular.module('combatTrackerFilters', []);


combatTrackerFilters.filter('players', function() {
  return function(input) {
    var players = [];
    input.forEach(function(character, idx) {
        if (character.is_player) {
            players.push(character);
        }
    });
    return players;
  };
});


combatTrackerFilters.filter('npcs', function() {
  return function(input) {
    var npcs = [];
    input.forEach(function(character, idx) {
        if (!character.is_player) {
            npcs.push(character);
        }
    });
    return npcs;
  };
});
