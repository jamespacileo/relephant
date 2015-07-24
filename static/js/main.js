(function() {
  var app;

  app = angular.module("DragonDemoApp", ['SwampDragonServices']);

  app.controller("GameCommentsCtrl", function($scope, $dragon) {
    $scope.todoList = {};
    $scope.todoItems = [];
    $scope.channel = 'global';
    $scope.comments = [];
    $scope.commentForm = {
      text: "",
      command: null
    };
    RPGJS.Materials = {
      "characters": {
        "1": "chara.png"
      }
    };
    RPGJS.defines({
      canvas: "game-canvas",
      autoload: false
    }).ready(function() {
      return RPGJS.Scene.map();
    });
    $scope.$watch("commentForm.text", function(newVal) {
      if (!newVal) {
        $scope.commentForm.command = null;
        return;
      }
      if (newVal.toLowerCase().indexOf("up") >= 0) {
        $scope.commentForm.command = "up";
        return;
      }
      if (newVal.toLowerCase().indexOf("down") >= 0) {
        $scope.commentForm.command = "down";
        return;
      }
      if (newVal.toLowerCase().indexOf("left") >= 0) {
        $scope.commentForm.command = "left";
        return;
      }
      if (newVal.toLowerCase().indexOf("right") >= 0) {
        $scope.commentForm.command = "right";
        return;
      }
      return $scope.commentForm.command = null;
    });
    swampdragon.ready(function() {
      console.log("ready");
      swampdragon.subscribe('game', $scope.channel, null, function(context, data) {
        console.log("subscribe", context, data);
        this.dataMapper = new DataMapper(data);
      });
      return swampdragon.onChannelMessage(function(channels, message) {
        var i;
        console.log("onChannelMessage", channels, message);
        $scope.comments.push(message.data);
        $scope.$apply();
        for (i in channels) {
          if (channels[i] === 'game-comment') {
            this.news = this.dataMapper.mapData(this.news, message.data);
          }
        }
      });
    });
    $scope.commentCreate = function($event) {
      $event.preventDefault();
      return swampdragon.callRouter('send_command', 'game', {
        comment: $scope.commentForm.text,
        command: $scope.commentForm.command
      }, function(context, data) {
        return console.log(context, data);
      }, function(context, data) {
        return console.log(context, data);
      });
    };
  });

}).call(this);
