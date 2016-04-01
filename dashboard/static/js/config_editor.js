angular.module('editorApp', [])
    .controller('EditorCtrl', function($scope) {

        $scope.configureEditor = function(editorId, lang) {
            console.log('init editor: ' + editorId);
            var theme = 'ace/theme/dawn';
            try {
                var editor = ace.edit(editorId);
                editor.setTheme(theme);
                editor.setShowPrintMargin(false);
                editor.setOptions({
                  fontFamily: "Lucida Console, Monaco, monospace",
                  fontSize: "10pt"
                });
                editor.getSession().setMode("ace/mode/" + lang);
            } catch (err) {
                console.log('probably cant find editor: ' + editorId)   ;
            }
        };

        $scope.configureEditor('recipients-editor', 'sql');
        $scope.configureEditor('html-template-editor', 'html');
        // TODO: only support 1 sheet now :-(
        $scope.configureEditor('sheet-editor', 'sql');

        $scope.postJson = function(url, data) {
            $.ajax({
                type: 'POST',
                url: url,
                data: JSON.stringify(data),
                contentType: "application/json",
                dataType: 'json'
            });
        };
        $scope.getEditorCode = function(editorId) {
            var editor = ace.edit(editorId);
            return editor.getValue();
        };

        $scope.send = function() {
            $scope.postJson('/api/command/', {command: 'send'});
            $.notify('Sending ...', 'info');
        };

        $scope.generate = function() {
            $scope.postJson('/api/command/', {command: 'generate'});
            $.notify('Generate ...', 'info');
        };

        $scope.save = function() {
            var recipients = $scope.getEditorCode('recipients-editor');
            var htmlTemplate = $scope.getEditorCode('html-template-editor');
            var sheetsSql = $scope.getEditorCode('sheet-editor');
            $scope.postJson(
                '/api/save_config/', 
                {
                    recipients: recipients,
                    html_template: htmlTemplate,
                    sheets_sql: sheetsSql,
                }
            )
            console.log(sheetsSql);
            console.log('data posted');
            $.notify('Config saved', 'success');
        };
    });