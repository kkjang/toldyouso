var my_app = angular.module('myapp', ['ng.django.urls', 'ngGrid', 'ui.bootstrap' /* dependencies */]).config(function($httpProvider, $locationProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
    $locationProvider.html5Mode({
        enabled: true,
    });
});

my_app.controller('RoomController', function($scope, $http, $window, djangoUrl, $location) {
    // console.log("location = ", $location);
    $scope.currentLocation = $location.absUrl();
    // console.log("outside of function, $location.absUrl() = ", $location.absUrl());
    // console.log("outside of function, $scope.absUrl = ", $scope.currentLocation);
    $scope.allBets = [];  
    $scope.processedBets = [];
    $scope.processedBet = [];

    //CODE RELATED TO SELECTING THE FILTER
    $scope.betFilterOptions = { title: "Bet Title",
                                challengerCondition: "Challenger Condition",
                                challengerAmount: "Challenger Amount",
                                challengedCondition: "Challenged Condition",
                                challengedAmount: "Challenged Amount", 
                                dateCreated: "Date Created", 
                                dateAccepted: "Date Accepted"};

    $scope.titleSelected = true; 
    $scope.challengerConditionSelected = false; 
    $scope.challengerAmountSelected = false; 
    $scope.challengedConditionSelected = false;
    $scope.challengedAmountSelected = false;
    $scope.dateCreatedSelected = false;
    $scope.dateAcceptedSelected = false; 


    //CONDITIONS THAT YOU'RE FILTERING BY
    $scope.searchBet = {title: "",
                        challengerCondition: "",
                        challengerAmount: "",
                        challengedCondition: "",
                        challengedAmount: "", 
                        dateCreated_start: "", 
                        dateCreated_end: "", 
                        dateAccepted_start: "",                       
                        dateAccepted_end: "",
                    };

    //SET UP DATE CALENDAR FILTER
    $scope.searchBet.dateCreated_start = new Date();    
    $scope.searchBet.dateCreated_end = new Date();
    $scope.searchBet.dateAccepted_start = new Date();
    $scope.searchBet.dateAccepted_end = new Date();

    $scope.format = 'dd-MMMM-yyyy';
    
    $scope.open = function($event, opened) {
        $event.preventDefault();
        $event.stopPropagation();
        $scope[opened] = true;
    };


    $scope.status = {
        isopen: false
    };

    $scope.resetSearchBet = function(){
        //RESET SELECTED OPTIONS
        $scope.titleSelected = false; 
        $scope.challengerConditionSelected = false; 
        $scope.challengerAmountSelected = false; 
        $scope.challengedConditionSelected = false;
        $scope.challengedAmountSelected = false;
        $scope.dateCreatedSelected = false;
        $scope.dateAcceptedSelected = false; 

        $scope.searchBet.title = "";
        $scope.searchBet.challengerCondition = "";
        $scope.searchBet.challengerAmount = "";
        $scope.searchBet.challengedCondition = "";
        $scope.searchBet.challengerAmount = "";
        $scope.searchBet.dateCreated_start = "";
        $scope.searchBet.dateCreated_end = "";
        $scope.searchBet.dateAccepted_start = "";
        $scope.searchBet.dateAccepted_end = "";
    }

    $scope.updateOptionsView = function(selectedFilter){
        
        $scope.resetSearchBet();
        
        if(selectedFilter === $scope.betFilterOptions.title){
            $scope.titleSelected = true; 
        }
        else if(selectedFilter === $scope.betFilterOptions.challengerCondition){
            $scope.challengerConditionSelected = true; 
        }
        else if(selectedFilter === $scope.betFilterOptions.challengerAmount){
            $scope.challengerAmountSelected = true; 
        }
        else if(selectedFilter === $scope.betFilterOptions.challengedCondition){
            $scope.challengedConditionSelected = true;
        }
        else if(selectedFilter === $scope.betFilterOptions.challengedAmount){
            $scope.challengedAmountSelected = true;
        }
        else if(selectedFilter === $scope.betFilterOptions.dateCreated){
            $scope.dateCreatedSelected = true;
            console.log("$scope.dateCreatedSelected = ",  $scope.dateCreatedSelected);

        }
        else if(selectedFilter === $scope.betFilterOptions.dateAccepted){
            $scope.dateAcceptedSelected = true;
            console.log("$scope.dateAcceptedSelected =", $scope.dateAcceptedSelected);
        }
    }

    
    //SETTING UP THE ROOMS TABLE 
    $scope.gridOptions = { data: 'processedBets',
                            showFilter : true,
                            enableColumnResize : true,
                            columnDefs:[
                            {field:'betTitle', displayName: 'Bet Title',         
                                cellTemplate: '<div class="ngCellText ng-scope col1 colt1" ng-click="displayBetContents()" ng-bind="row.getProperty(col.field)"></div>'},
                            {field:'challengerCondition', displayName: "Challenger Condition"},
                            {field:'challengerAmount', displayName: "Challenger Amount"},
                            {field:'challengedCondition', displayName: "Challenged Condition"}, 
                            {field:'challengedAmount', displayName: "Challenged Amount"},
                            {field:'dateCreated', displayName: "Date Created"},
                            {field:'dateAccepted', displayName: "Date Accepted"}
                           ]
                       };

    $scope.submit = function() {
        var in_data = angular.toJson($scope.bet_data);
        $http.post(djangoUrl.reverse('bet-list'), in_data)
            .success(function(out_data) {
                console.log("Success");
                console.log(out_data);
                $window.location.href = djangoUrl.reverse('thanks');
            });
    }

    $scope.getKeyFromUrl = function(){
        console.log('current $location.absUrl = ', $scope.currentLocation);
        console.log('inside function, $location = ', $location);
        $http({ //toldyouso.com/room/rooms/1?title=abc
            url: $location.absUrl, //toldyouso.com/room/rooms/1
            method: "GET",
            params: {title: $location.search()} //CONTINUE HERE! Not sure what to put here!abc
        })
        .success(function (data){
            console.log(data);
            console.log(djangoUrl.reverse('room-list'));
            $scope.theBetKey = data.results; 
    });
    }

    $scope.processBets = function(data){
        $scope.allBets = data.results;
        console.log('WEE　$scope.allBets = ', $scope.allBets);
        $scope.processedBets = []; // clear list

        var i = 0;
        for(i = 0; i <$scope.allBets.length; i++){
            $scope.processedBet = [];
            $scope.processedBet.betTitle = $scope.allBets[i].title;
            $scope.processedBet.dateCreated = $scope.allBets[i].date_created;
            $scope.processedBet.dateAccepted = $scope.allBets[i].date_accepted;
            if($scope.allBets[i].wagers[0].user_id === $scope.allBets[i].creator_id){
                //ADD CONDITION TO CHECK IF 2ND USER IS NULL
                $scope.processedBet.creatorUserId = $scope.allBets[i].wagers[0].user_id; 
                $scope.processedBet.challengerCondition = $scope.allBets[i].wagers[0].condition;
                $scope.processedBet.challengerAmount = $scope.allBets[i].wagers[0].amount;
                $scope.processedBet.challengedCondition = $scope.allBets[i].wagers[1].condition;
                $scope.processedBet.challengedAmount = $scope.allBets[i].wagers[1].amount;
            }
            else if ($scope.allBets[i].wagers[1].user_id === $scope.allBets[i].creator_id){
                $scope.processedBet.creatorUserId = $scope.allBets[i].wagers[0].user_id; 
                $scope.processedBet.challengerAmount = $scope.allBets[i].wagers[1].amount;
                $scope.processedBet.challengerCondition = $scope.allBets[i].wagers[1].condition; 
                $scope.processedBet.challengedCondition = $scope.allBets[i].wagers[0].condition;
                $scope.processedBet.challengedAmount = $scope.allBets[i].wagers[0].amount;
            }
            // console.log("$scope.processedBet = ", $scope.processedBet); 
            $scope.processedBets.push($scope.processedBet);  
        }
        console.log("$scope.processedBets = ", $scope.processedBets);
    }

    $scope.getAllBets = function(){
        $http.get(djangoUrl.reverse('bet-list'))
            .success(function (data){
                $scope.processBets(data);
            });
    }

    $scope.getBet = function(){
        var bet_id = $location.path().split('/')[2];
        $http.get(djangoUrl.reverse('bet-detail', {'pk':bet_id}))
            .then(function (response) {
                console.log(response);
                $scope.bet_data = response.data; 
                console.log('$scope.bet_data = ', $scope.bet_data);
                console.log($scope);
            }, function(response) {
                console.log(response);
                if (response.status == 403){
                    $window.location.href = djangoUrl.reverse('403_error');
                }
            });
    }

    $scope.getBetWithKey = function(){
        var bet_id = $location.path().split('/')[2];
        var search_vars = $location.search();
        var key = search_vars['key'];
        $http.get(djangoUrl.reverse('bet-detail', {'pk':bet_id}) + '&key=' + key)
            .then(function (response) {
                console.log(response);
                $scope.bet_data = response.data; 
                console.log('$scope.bet_data = ', $scope.bet_data);
                console.log($scope);
            }, function(response) {
                console.log(response);
                if (response.status == 403){
                    $window.location.href = djangoUrl.reverse('403_error');
                }
            });
    }

    $scope.acceptBet = function(){
        console.log("NEW SCOPE");
        console.log($scope);
        var today = new Date();
        var dd = today.getDate();
        var mm = today.getMonth()+1; //January is 0!
        var yyyy = today.getFullYear();
        if(dd<10) {
            dd='0'+dd
        } 

        if(mm<10) {
            mm='0'+mm
        } 
        today = yyyy + '-' + mm+'-'+dd;
        var update_data = {'date_accepted': today}
        var bet_id = $location.path().split('/')[2];
        $http.patch(djangoUrl.reverse('bet-detail', {'pk':bet_id}), update_data)
            .then(function (response) {
                console.log(response);
                $scope.bet_data = response.data; 
                console.log('$scope.bet_data = ', $scope.bet_data);
                console.log($scope);
            }, function(response) {
                console.log(response);
                if (response.status == 403){
                    $window.location.href = djangoUrl.reverse('403_error');
                }
            });
    }


    $scope.filterBets = function(){
        console.log("filtering bets");
        console.log($scope.searchBet);
        var query_string = djangoUrl.reverse('bet-list');
        var update_bets = true;

        if($scope.titleSelected){
            query_string += '&title=' + $scope.searchBet.title;
            console.log("title selected");
        }
        else if($scope.challengerConditionSelected){
            // query_string = "/wagers" + djangoUrl.reverse('bet-list');
            query_string += '&condition=' + $scope.searchBet.challengerCondition + '&creator=true';
        }
        else if($scope.challengerAmountSelected){
            query_string += '&amount=' + $scope.searchBet.challengerAmount + '&creator=true';
        }
        else if($scope.selectedFilter === $scope.betFilterOptions.challengedCondition){
            query_string += '&condition=' + $scope.searchBet.challengedCondition + '&creator=false';
        }
        else if($scope.challengedAmountSelected){
            query_string += '&amount=' + $scope.searchBet.challengedAmount + '&creator=true';
        }
        else if($scope.dateCreatedSelected){
            query_string += '&date_created_start=' + $scope.searchBet.dateCreated_start.getFullYear() + '-' + $scope.searchBet.dateCreated_start.getMonth() + '-' + $scope.searchBet.dateCreated_start.getDate() + '&date_created_end=' + $scope.searchBet.dateCreated_end.getFullYear() + '-' + $scope.searchBet.dateCreated_end.getMonth() + '-' + $scope.searchBet.dateCreated_end.getDate();
        }
        else if($scope.dateAcceptedSelected){
            query_string += '&date_accept_start=' + $scope.searchBet.dateAccepted_start.getFullYear() + '-' + $scope.searchBet.dateAccepted_start.getMonth() + '-' + $scope.searchBet.dateAccepted_start.getDate() + '&date_accepted_end=' + $scope.searchBet.dateAccepted_end.getFullYear() + '-' + $scope.searchBet.dateAccepted_end.getMonth() + '-' + $scope.searchBet.dateAccepted_end.getDate();
        }
        else {
            update_bets = false;
        }
        //query_string = "" + djangoUrl.reverse('bet-list') + '?datetime_field__lt=2010-09-28+21:00:59&datetime_field__gt=2010-09-22+00:00:00'

        if (update_bets){
        $http.get(query_string) // creates dynamic URL, sends in filter
            .success(function (data){
                console.log("with query_string = ", query_string, "data after filtering = ", data);
                $scope.processBets(data);
                // console.log("done!");
            });
        }
    }

    // $scope.getBetsByTitle = function(){
    //     console.log("djrev = ", djangoUrl.reverse('bet-list'));
    //     var query_string = djangoUrl.reverse('bet-list');
    //     query_string += '&title=' + $scope.searchBet.title;
    //     console.log("query_string = ", query_string)
    //     $http.get(query_string) // creates dynamic URL, sends in filter
    //         .success(function (data){
    //             $scope.allBets = data.results;
    //             console.log("done!");
    //         });
    // }


    //setinstone.com/angular/reverse/bet-list?title=asdf
});