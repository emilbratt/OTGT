<?php
declare(strict_types=1);
// SPDX-FileCopyrightText: Emil Bratt Børsting <emilbratt@gmail.com>
// SPDX-License-Identifier: AGPL-3.0-or-later

namespace OCA\VareInfo\AppInfo;

use OCP\AppFramework\App;

class Application extends App {
	public const APP_ID = 'vareinfo';

	public function __construct() {
		parent::__construct(self::APP_ID);
	}
}
