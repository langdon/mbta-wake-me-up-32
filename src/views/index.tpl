<style>
#feedback { font-size: 1.4em; }
#selectable .ui-selecting { background: #FECA40; }
#selectable .ui-selected { background: #F39814; color: white; }
#selectable { list-style-type: none; margin: 0; padding: 0; width: 60%; }
#selectable li { margin: 3px; padding: 0.4em; font-size: 1.4em; height: 18px; }
</style>
<script>
</script>
<div id="content-area">
	<h2 id="directions">Choose the train you managed to get on:</h2>
	<ol id="selectable">
		<li class="ui-widget-content" train-id="1">Item 1</li>
		<li class="ui-widget-content" train-id="2">Item 2</li>
	</ol>
</div>


%rebase layout title='Main', page_includes='<script src="/scripts/wake-me-up.js" type="text/javascript" charset="utf-8"></script>'
