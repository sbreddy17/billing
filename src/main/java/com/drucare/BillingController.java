package com.drucare;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class BillingController {
	@GetMapping("/")
	public String billing() {
		return "Welcome to billing version One";
	}

}
