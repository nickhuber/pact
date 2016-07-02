var characterServices = angular.module('characterServices', ['ngResource']);

characterServices.factory('Character', ['$resource', function($resource) {
    return $resource(
        'api/characters/:id/',
        {id: '@id'},
        {
            update: {method: 'PATCH'}
        }
    );
}]);

characterServices.factory('PlayerCharacter', ['$resource', function($resource) {
    return $resource(
        'api/characters/:id/?is_player=True',
        {id: '@id'},
        {
            update: {method: 'PATCH'}
        }
    );
}]);

characterServices.factory('NonPlayerCharacter', ['$resource', function($resource) {
    return $resource(
        'api/characters/:id/?is_player=False',
        {id: '@id'},
        {
            update: {method: 'PATCH'}
        }
    );
}]);
