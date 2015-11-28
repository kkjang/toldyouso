var my_app = angular.module('myapp', ['ng.django.urls', /* dependencies */]).config(function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
});

my_app.controller('RoomController', function($scope, $http, $window, djangoUrl) {

    $scope.submit = function() {
        var in_data = angular.toJson($scope.room_data);
        console.log($scope);
        $http.post(djangoUrl.reverse('room-list'), in_data)
            .success(function(out_data) {
                console.log("Success");
                console.log(out_data);
                $window.location.href = djangoUrl.reverse('thanks');
            });
    }

    $scope.getAllRooms = function(){
        $http.get(djangoUrl.reverse('room-list'))
            .success(function (data){
                console.log(data);
                $scope.allRooms = data.results; 
                console.log('$scope.allRooms = ', $scope.allRooms);
            })
    }
});