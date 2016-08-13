(function() {
    'use strict';
    var characterServices = angular.module('characterServices', ['ngResource']);

    characterServices.factory('Character', ['$resource', function($resource) {
        return $resource(
            'api/characters/:uuid/',
            {uuid: '@uuid'},
            {
                update: {method: 'PATCH'}
            }
        );
    }]);

    characterServices.factory('PlayerCharacter', ['$resource', function($resource) {
        return $resource(
            'api/characters/:uuid/?is_player=True',
            {uuid: '@uuid'},
            {
                update: {method: 'PATCH'}
            }
        );
    }]);

    characterServices.factory('NonPlayerCharacter', ['$resource', function($resource) {
        return $resource(
            'api/characters/:uuid/?is_player=False',
            {uuid: '@uuid'},
            {
                update: {method: 'PATCH'}
            }
        );
    }]);
})();
