CREATE SCHEMA icl
    AUTHORIZATION postgres;

CREATE TABLE icl.htmlrequests
(
    xrequestid uuid NOT NULL,
    "time" character varying COLLATE pg_catalog."default",
    version character varying COLLATE pg_catalog."default",
    product character varying COLLATE pg_catalog."default",
    application character varying COLLATE pg_catalog."default",
    applicationversion character varying COLLATE pg_catalog."default",
    buildversion character varying COLLATE pg_catalog."default",
    environment character varying COLLATE pg_catalog."default",
    backendregion character varying COLLATE pg_catalog."default",
    origin character varying COLLATE pg_catalog."default",
    channel character varying COLLATE pg_catalog."default",
    path character varying COLLATE pg_catalog."default",
    method character varying COLLATE pg_catalog."default",
    useragent character varying COLLATE pg_catalog."default",
    CONSTRAINT requests_pkey PRIMARY KEY (xrequestid)
)

TABLESPACE pg_default;

ALTER TABLE icl.htmlrequests
    OWNER to postgres;

CREATE TABLE icl.service
(
    serviceid uuid NOT NULL,
    serviceprovidername character varying COLLATE pg_catalog."default",
    servicemaintype character varying COLLATE pg_catalog."default",
    starttime character varying COLLATE pg_catalog."default",
    endtime character varying COLLATE pg_catalog."default",
    predictedstarttime character varying COLLATE pg_catalog."default",
    predictedendtime character varying COLLATE pg_catalog."default",
    CONSTRAINT service_pkey PRIMARY KEY (serviceid)
)

TABLESPACE pg_default;

ALTER TABLE icl.service
    OWNER to postgres;

CREATE TABLE icl.sub
(
    subid uuid NOT NULL,
    vin character varying COLLATE pg_catalog."default",
    servicestatus character varying COLLATE pg_catalog."default",
    startlocationlongitude character varying COLLATE pg_catalog."default",
    startlocationlatitude character varying COLLATE pg_catalog."default",
    endlocationlongitude character varying COLLATE pg_catalog."default",
    endlocationlatitude character varying COLLATE pg_catalog."default",
    serviceid uuid,
    CONSTRAINT sub_pkey PRIMARY KEY (subid),
    CONSTRAINT service_fkey FOREIGN KEY (serviceid)
        REFERENCES icl.service (serviceid) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
)

TABLESPACE pg_default;

ALTER TABLE icl.sub
    OWNER to postgres;

CREATE TABLE icl.requests
(
    requestid uuid NOT NULL,
    serviceid uuid,
    CONSTRAINT requests_pkey1 PRIMARY KEY (requestid),
    CONSTRAINT service_fkey FOREIGN KEY (serviceid)
        REFERENCES icl.service (serviceid) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
)

TABLESPACE pg_default;

ALTER TABLE icl.requests
    OWNER to postgres;

CREATE TABLE icl.event
(
    id uuid NOT NULL,
    "time" character varying COLLATE pg_catalog."default",
    privacyclass character varying COLLATE pg_catalog."default",
    flowid uuid,
    xrequestid uuid,
    contentcategory character varying COLLATE pg_catalog."default",
    CONSTRAINT event_pkey PRIMARY KEY (id),
    CONSTRAINT "flowId_fkey" FOREIGN KEY (flowid)
        REFERENCES icl.requests (requestid) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID,
    CONSTRAINT "xRequest_fkey" FOREIGN KEY (xrequestid)
        REFERENCES icl.htmlrequests (xrequestid) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
)

TABLESPACE pg_default;

ALTER TABLE icl.event
    OWNER to postgres;

