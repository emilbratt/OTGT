<?php
declare(strict_types=1);
// SPDX-FileCopyrightText: Emil Bratt Børsting <emilbratt@gmail.com>
// SPDX-License-Identifier: AGPL-3.0-or-later
// print out strings using either print_unescaped() or p()

$hello_world = <<<EOT
<h2>hello world</h2>
EOT;
print_unescaped($hello_world);

?>

<div id="content"></div>
