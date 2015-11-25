var my_app = angular.module('myapp', [/* dependencies */]).config(function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});

my_app.controller('RoomController', function($scope, $http) {
    $scope.submit = function() {
        var in_data = angular.toJson($scope.room_data);
        console.log(in_data);
        $http.post('/rooms/', in_data)
            .success(function(out_data) {
                console.log("Success");
            });
    }
});