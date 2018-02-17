<html>
    <head>
        <title>{{ title or "Highlighter" }}</title>
        <link rel="icon" type="image/png" href="/static/icons/favicon.png" />

        <link rel="stylesheet" href="//cdnjs.cloudflare.com/ajax/libs/materialize/0.98.2/css/materialize.min.css">
        <link rel="stylesheet" href="//fonts.googleapis.com/icon?family=Material+Icons">
        <link rel="stylesheet" href="//fonts.googleapis.com/css?family=Open+Sans:300,300i">
        <link rel="stylesheet" href="/static/css/content.css">

        <script src="//ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
        <script src="//cdnjs.cloudflare.com/ajax/libs/materialize/0.98.2/js/materialize.min.js"></script>

        <script src="//cdnjs.cloudflare.com/ajax/libs/rangy/1.3.0/rangy-core.min.js"></script>
        <script src="//cdnjs.cloudflare.com/ajax/libs/rangy/1.3.0/rangy-classapplier.min.js"></script>
        <script src="//cdnjs.cloudflare.com/ajax/libs/rangy/1.3.0/rangy-textrange.min.js"></script>
        % if page_script:
            <script src="/static/js/{{ page_script }}"></script>
        % end
    </head>

    <body>
        <script src="/static/js/ga.js"></script>
        <header></header>
        <main>{{! base }}</main>
        <footer></footer>
    </body>

</html>
