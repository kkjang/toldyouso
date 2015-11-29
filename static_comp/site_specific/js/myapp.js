var my_app = angular.module('myapp', ['ng.django.urls', /* dependencies */]).config(function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
});

my_app.controller('RoomController', function($scope, $http, $window, $location, djangoUrl) {

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

    $scope.getKeyFromUrl = function($location){
            console.log($location);
            console.log($location.search().q);
            $http({ //toldyouso.com/room/rooms/1?title=abc
                url: user.details_path, //toldyouso.com/room/rooms/1
                method: "GET",
                params: {title: $location.search()} //abc
             })
            .success(function (data){
                console.log(data);
                console.log(djangoUrl.reverse('room-list'));
                $scope.allRooms = data.results; 
                console.log('$scope.allRooms = ', $scope.allRooms);
            })
    }
});