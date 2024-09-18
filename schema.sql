-- Auto Generated From Sqlalchemy an ORM
CREATE TABLE IF NOT EXISTS "order" (
	id VARCHAR(36) NOT NULL, 
	"referenceNumId" VARCHAR(36) NOT NULL, 
	"countryCodeId" VARCHAR(36) NOT NULL, 
	"addressId" VARCHAR(36) NOT NULL, 
	"customerId" VARCHAR(36) NOT NULL, 
	"orderLinesId" VARCHAR(36) NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY("referenceNumId") REFERENCES "order" (id), 
	FOREIGN KEY("countryCodeId") REFERENCES "order" (id), 
	FOREIGN KEY("addressId") REFERENCES "order" (id), 
	FOREIGN KEY("customerId") REFERENCES "order" (id), 
	FOREIGN KEY("orderLinesId") REFERENCES "order" (id)
);
CREATE TABLE reference_num (
	id VARCHAR(36) NOT NULL, 
	"orderId" VARCHAR(36) NOT NULL, 
	num VARCHAR(30) NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY("orderId") REFERENCES "order" (id), 
	UNIQUE (num)
);
CREATE TABLE country_code (
	id VARCHAR(36) NOT NULL, 
	"orderId" VARCHAR(36) NOT NULL, 
	code VARCHAR(30) NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY("orderId") REFERENCES "order" (id)
);
CREATE TABLE address (
	id VARCHAR(36) NOT NULL, 
	"orderId" VARCHAR(36) NOT NULL, 
	"fullName" VARCHAR(30) NOT NULL, 
	"addressType" VARCHAR(30) NOT NULL, 
	"addressLine1" VARCHAR(30) NOT NULL, 
	"addressLine2" VARCHAR(30) NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY("orderId") REFERENCES "order" (id)
);
CREATE TABLE customer (
	id VARCHAR(36) NOT NULL, 
	"orderId" VARCHAR(36) NOT NULL, 
	"customerCode" VARCHAR(50) NOT NULL, 
	"firstName" VARCHAR(50) NOT NULL, 
	"lastName" VARCHAR(50) NOT NULL, 
	phone VARCHAR(50) NOT NULL, 
	email VARCHAR(50) NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY("orderId") REFERENCES "order" (id)
);
CREATE TABLE order_lines (
	id VARCHAR(36) NOT NULL, 
	"orderId" VARCHAR(36) NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY("orderId") REFERENCES "order" (id)
);
CREATE TABLE order_line (
	id VARCHAR(36) NOT NULL, 
	"itemNum" VARCHAR(30) NOT NULL, 
	"itemDescription" VARCHAR(30) NOT NULL, 
	"orderLinesId" VARCHAR(36) NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY("orderLinesId") REFERENCES order_lines (id)
);
