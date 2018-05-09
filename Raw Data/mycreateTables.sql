CREATE TABLE Sector
(
    sector_ID INT PRIMARY KEY AUTO_INCREMENT,
    sector NVARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE Industry
(
    industry_ID INT PRIMARY KEY AUTO_INCREMENT,
    industry NVARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE CeoTitle
(
    ceo_title_ID INT PRIMARY KEY AUTO_INCREMENT,
    title NVARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE Company
(
    company_ID INT PRIMARY KEY AUTO_INCREMENT,
    title NVARCHAR(255) UNIQUE NOT NULL,
    website NVARCHAR(255),
    ceo NVARCHAR(255),
    employees INT,
    sector_ID INT,
    industry_ID INT,
    ceo_title_ID INT,
    FOREIGN KEY (sector_ID) REFERENCES Sector(sector_ID) ON DELETE RESTRICT,
    FOREIGN KEY (industry_ID) REFERENCES Industry(industry_ID) ON DELETE RESTRICT,
    FOREIGN KEY (ceo_title_ID) REFERENCES CeoTitle(ceo_title_ID) ON DELETE RESTRICT
);

CREATE TABLE HQ
(
    company_ID INT PRIMARY KEY NOT NULL,
    street NVARCHAR(255),
    city NVARCHAR(255),
    hq_state NVARCHAR(255),
    zip NVARCHAR(255),
    phone NVARCHAR(255) UNIQUE,
	  UNIQUE (street, city, hq_state, zip),
    FOREIGN KEY (company_ID) REFERENCES Company(company_ID) ON DELETE RESTRICT
);

CREATE TABLE Alias
(
    company_ID INT PRIMARY KEY NOT NULL,
    ticker NVARCHAR(255),
    full_name NVARCHAR(255) UNIQUE,
    FOREIGN KEY (company_ID) REFERENCES Company(company_ID) ON DELETE RESTRICT
);

CREATE TABLE YearRank
(
    company_ID INT NOT NULL,
    year INT NOT NULL,
    ranking INT,
    revenues DECIMAL(8, 2),
    profits DECIMAL(8, 2),
    assets DECIMAL(9, 2),
    PRIMARY KEY (company_ID, year),
    FOREIGN KEY (company_ID) REFERENCES Company(company_ID) ON DELETE RESTRICT
);
