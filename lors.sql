--
-- PostgreSQL database dump
--

\restrict zB4aminOi4xmJF2dYyQhcKehc1WElsIRfuqERc4E8vbSRh5j1B0entC1lw7SmmC

-- Dumped from database version 17.9 (Homebrew)
-- Dumped by pg_dump version 17.9 (Homebrew)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

ALTER TABLE IF EXISTS ONLY public.lors_complaintphoto DROP CONSTRAINT IF EXISTS lors_complaintphoto_complaint_id_c92316d9_fk_lors_complaint_id;
ALTER TABLE IF EXISTS ONLY public.lors_complaint DROP CONSTRAINT IF EXISTS lors_complaint_car_model_id_051e12ce_fk_lors_carmodel_id;
ALTER TABLE IF EXISTS ONLY public.lors_carmodel DROP CONSTRAINT IF EXISTS lors_carmodel_brand_id_00a4ade4_fk_lors_brand_id;
ALTER TABLE IF EXISTS ONLY public.django_admin_log DROP CONSTRAINT IF EXISTS django_admin_log_user_id_c564eba6_fk_auth_user_id;
ALTER TABLE IF EXISTS ONLY public.django_admin_log DROP CONSTRAINT IF EXISTS django_admin_log_content_type_id_c4bce8eb_fk_django_co;
ALTER TABLE IF EXISTS ONLY public.auth_user_user_permissions DROP CONSTRAINT IF EXISTS auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id;
ALTER TABLE IF EXISTS ONLY public.auth_user_user_permissions DROP CONSTRAINT IF EXISTS auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm;
ALTER TABLE IF EXISTS ONLY public.auth_user_groups DROP CONSTRAINT IF EXISTS auth_user_groups_user_id_6a12ed8b_fk_auth_user_id;
ALTER TABLE IF EXISTS ONLY public.auth_user_groups DROP CONSTRAINT IF EXISTS auth_user_groups_group_id_97559544_fk_auth_group_id;
ALTER TABLE IF EXISTS ONLY public.auth_permission DROP CONSTRAINT IF EXISTS auth_permission_content_type_id_2f476e4b_fk_django_co;
ALTER TABLE IF EXISTS ONLY public.auth_group_permissions DROP CONSTRAINT IF EXISTS auth_group_permissions_group_id_b120cbf9_fk_auth_group_id;
ALTER TABLE IF EXISTS ONLY public.auth_group_permissions DROP CONSTRAINT IF EXISTS auth_group_permissio_permission_id_84c5c92e_fk_auth_perm;
DROP INDEX IF EXISTS public.lors_complaintphoto_complaint_id_c92316d9;
DROP INDEX IF EXISTS public.lors_complaint_car_model_id_051e12ce;
DROP INDEX IF EXISTS public.lors_carmodel_brand_id_00a4ade4;
DROP INDEX IF EXISTS public.lors_brand_name_aa56162e_like;
DROP INDEX IF EXISTS public.django_session_session_key_c0390e0f_like;
DROP INDEX IF EXISTS public.django_session_expire_date_a5c62663;
DROP INDEX IF EXISTS public.django_admin_log_user_id_c564eba6;
DROP INDEX IF EXISTS public.django_admin_log_content_type_id_c4bce8eb;
DROP INDEX IF EXISTS public.auth_user_username_6821ab7c_like;
DROP INDEX IF EXISTS public.auth_user_user_permissions_user_id_a95ead1b;
DROP INDEX IF EXISTS public.auth_user_user_permissions_permission_id_1fbb5f2c;
DROP INDEX IF EXISTS public.auth_user_groups_user_id_6a12ed8b;
DROP INDEX IF EXISTS public.auth_user_groups_group_id_97559544;
DROP INDEX IF EXISTS public.auth_permission_content_type_id_2f476e4b;
DROP INDEX IF EXISTS public.auth_group_permissions_permission_id_84c5c92e;
DROP INDEX IF EXISTS public.auth_group_permissions_group_id_b120cbf9;
DROP INDEX IF EXISTS public.auth_group_name_a6ea08ec_like;
ALTER TABLE IF EXISTS ONLY public.lors_sitesettings DROP CONSTRAINT IF EXISTS lors_sitesettings_pkey;
ALTER TABLE IF EXISTS ONLY public.lors_review DROP CONSTRAINT IF EXISTS lors_review_pkey;
ALTER TABLE IF EXISTS ONLY public.lors_complaintphoto DROP CONSTRAINT IF EXISTS lors_complaintphoto_pkey;
ALTER TABLE IF EXISTS ONLY public.lors_complaint DROP CONSTRAINT IF EXISTS lors_complaint_pkey;
ALTER TABLE IF EXISTS ONLY public.lors_carmodel DROP CONSTRAINT IF EXISTS lors_carmodel_sheet_row_d3a9bf9b_uniq;
ALTER TABLE IF EXISTS ONLY public.lors_carmodel DROP CONSTRAINT IF EXISTS lors_carmodel_pkey;
ALTER TABLE IF EXISTS ONLY public.lors_brand DROP CONSTRAINT IF EXISTS lors_brand_pkey;
ALTER TABLE IF EXISTS ONLY public.lors_brand DROP CONSTRAINT IF EXISTS lors_brand_name_key;
ALTER TABLE IF EXISTS ONLY public.django_session DROP CONSTRAINT IF EXISTS django_session_pkey;
ALTER TABLE IF EXISTS ONLY public.django_migrations DROP CONSTRAINT IF EXISTS django_migrations_pkey;
ALTER TABLE IF EXISTS ONLY public.django_content_type DROP CONSTRAINT IF EXISTS django_content_type_pkey;
ALTER TABLE IF EXISTS ONLY public.django_content_type DROP CONSTRAINT IF EXISTS django_content_type_app_label_model_76bd3d3b_uniq;
ALTER TABLE IF EXISTS ONLY public.django_admin_log DROP CONSTRAINT IF EXISTS django_admin_log_pkey;
ALTER TABLE IF EXISTS ONLY public.auth_user DROP CONSTRAINT IF EXISTS auth_user_username_key;
ALTER TABLE IF EXISTS ONLY public.auth_user_user_permissions DROP CONSTRAINT IF EXISTS auth_user_user_permissions_user_id_permission_id_14a6b632_uniq;
ALTER TABLE IF EXISTS ONLY public.auth_user_user_permissions DROP CONSTRAINT IF EXISTS auth_user_user_permissions_pkey;
ALTER TABLE IF EXISTS ONLY public.auth_user DROP CONSTRAINT IF EXISTS auth_user_pkey;
ALTER TABLE IF EXISTS ONLY public.auth_user_groups DROP CONSTRAINT IF EXISTS auth_user_groups_user_id_group_id_94350c0c_uniq;
ALTER TABLE IF EXISTS ONLY public.auth_user_groups DROP CONSTRAINT IF EXISTS auth_user_groups_pkey;
ALTER TABLE IF EXISTS ONLY public.auth_permission DROP CONSTRAINT IF EXISTS auth_permission_pkey;
ALTER TABLE IF EXISTS ONLY public.auth_permission DROP CONSTRAINT IF EXISTS auth_permission_content_type_id_codename_01ab375a_uniq;
ALTER TABLE IF EXISTS ONLY public.auth_group DROP CONSTRAINT IF EXISTS auth_group_pkey;
ALTER TABLE IF EXISTS ONLY public.auth_group_permissions DROP CONSTRAINT IF EXISTS auth_group_permissions_pkey;
ALTER TABLE IF EXISTS ONLY public.auth_group_permissions DROP CONSTRAINT IF EXISTS auth_group_permissions_group_id_permission_id_0cd325b0_uniq;
ALTER TABLE IF EXISTS ONLY public.auth_group DROP CONSTRAINT IF EXISTS auth_group_name_key;
ALTER TABLE IF EXISTS ONLY public.assistant_botmessage DROP CONSTRAINT IF EXISTS assistant_botmessage_pkey;
DROP TABLE IF EXISTS public.lors_sitesettings;
DROP TABLE IF EXISTS public.lors_review;
DROP TABLE IF EXISTS public.lors_complaintphoto;
DROP TABLE IF EXISTS public.lors_complaint;
DROP TABLE IF EXISTS public.lors_carmodel;
DROP TABLE IF EXISTS public.lors_brand;
DROP TABLE IF EXISTS public.django_session;
DROP TABLE IF EXISTS public.django_migrations;
DROP TABLE IF EXISTS public.django_content_type;
DROP TABLE IF EXISTS public.django_admin_log;
DROP TABLE IF EXISTS public.auth_user_user_permissions;
DROP TABLE IF EXISTS public.auth_user_groups;
DROP TABLE IF EXISTS public.auth_user;
DROP TABLE IF EXISTS public.auth_permission;
DROP TABLE IF EXISTS public.auth_group_permissions;
DROP TABLE IF EXISTS public.auth_group;
DROP TABLE IF EXISTS public.assistant_botmessage;
SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: assistant_botmessage; Type: TABLE; Schema: public; Owner: lors_user
--

CREATE TABLE public.assistant_botmessage (
    id bigint NOT NULL,
    channel character varying(20) NOT NULL,
    external_user_id character varying(100) NOT NULL,
    direction character varying(3) NOT NULL,
    text text NOT NULL,
    created_at timestamp with time zone NOT NULL
);


ALTER TABLE public.assistant_botmessage OWNER TO lors_user;

--
-- Name: assistant_botmessage_id_seq; Type: SEQUENCE; Schema: public; Owner: lors_user
--

ALTER TABLE public.assistant_botmessage ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.assistant_botmessage_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: lors_user
--

CREATE TABLE public.auth_group (
    id integer NOT NULL,
    name character varying(150) NOT NULL
);


ALTER TABLE public.auth_group OWNER TO lors_user;

--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: lors_user
--

ALTER TABLE public.auth_group ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_group_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: lors_user
--

CREATE TABLE public.auth_group_permissions (
    id bigint NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_group_permissions OWNER TO lors_user;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: lors_user
--

ALTER TABLE public.auth_group_permissions ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_group_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: lors_user
--

CREATE TABLE public.auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


ALTER TABLE public.auth_permission OWNER TO lors_user;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: lors_user
--

ALTER TABLE public.auth_permission ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_permission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_user; Type: TABLE; Schema: public; Owner: lors_user
--

CREATE TABLE public.auth_user (
    id integer NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    is_superuser boolean NOT NULL,
    username character varying(150) NOT NULL,
    first_name character varying(150) NOT NULL,
    last_name character varying(150) NOT NULL,
    email character varying(254) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL
);


ALTER TABLE public.auth_user OWNER TO lors_user;

--
-- Name: auth_user_groups; Type: TABLE; Schema: public; Owner: lors_user
--

CREATE TABLE public.auth_user_groups (
    id bigint NOT NULL,
    user_id integer NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE public.auth_user_groups OWNER TO lors_user;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: lors_user
--

ALTER TABLE public.auth_user_groups ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_user_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_user_id_seq; Type: SEQUENCE; Schema: public; Owner: lors_user
--

ALTER TABLE public.auth_user ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_user_user_permissions; Type: TABLE; Schema: public; Owner: lors_user
--

CREATE TABLE public.auth_user_user_permissions (
    id bigint NOT NULL,
    user_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_user_user_permissions OWNER TO lors_user;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: lors_user
--

ALTER TABLE public.auth_user_user_permissions ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_user_user_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: lors_user
--

CREATE TABLE public.django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id integer NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


ALTER TABLE public.django_admin_log OWNER TO lors_user;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: lors_user
--

ALTER TABLE public.django_admin_log ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_admin_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: lors_user
--

CREATE TABLE public.django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


ALTER TABLE public.django_content_type OWNER TO lors_user;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: lors_user
--

ALTER TABLE public.django_content_type ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_content_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: lors_user
--

CREATE TABLE public.django_migrations (
    id bigint NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


ALTER TABLE public.django_migrations OWNER TO lors_user;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: lors_user
--

ALTER TABLE public.django_migrations ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_migrations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_session; Type: TABLE; Schema: public; Owner: lors_user
--

CREATE TABLE public.django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


ALTER TABLE public.django_session OWNER TO lors_user;

--
-- Name: lors_brand; Type: TABLE; Schema: public; Owner: lors_user
--

CREATE TABLE public.lors_brand (
    id bigint NOT NULL,
    name character varying(100) NOT NULL
);


ALTER TABLE public.lors_brand OWNER TO lors_user;

--
-- Name: lors_brand_id_seq; Type: SEQUENCE; Schema: public; Owner: lors_user
--

ALTER TABLE public.lors_brand ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.lors_brand_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: lors_carmodel; Type: TABLE; Schema: public; Owner: lors_user
--

CREATE TABLE public.lors_carmodel (
    id bigint NOT NULL,
    name character varying(255) NOT NULL,
    template_code character varying(50) NOT NULL,
    car_type character varying(255) NOT NULL,
    driver_cut character varying(255) NOT NULL,
    package character varying(255) NOT NULL,
    second_row_package character varying(255) NOT NULL,
    notes text NOT NULL,
    video_url character varying(500) NOT NULL,
    sheet_row integer,
    brand_id bigint NOT NULL,
    CONSTRAINT lors_carmodel_sheet_row_check CHECK ((sheet_row >= 0))
);


ALTER TABLE public.lors_carmodel OWNER TO lors_user;

--
-- Name: lors_carmodel_id_seq; Type: SEQUENCE; Schema: public; Owner: lors_user
--

ALTER TABLE public.lors_carmodel ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.lors_carmodel_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: lors_complaint; Type: TABLE; Schema: public; Owner: lors_user
--

CREATE TABLE public.lors_complaint (
    id bigint NOT NULL,
    name character varying(150) NOT NULL,
    phone character varying(32) NOT NULL,
    text text NOT NULL,
    status character varying(20) NOT NULL,
    created_at timestamp with time zone NOT NULL,
    car_model_id bigint
);


ALTER TABLE public.lors_complaint OWNER TO lors_user;

--
-- Name: lors_complaint_id_seq; Type: SEQUENCE; Schema: public; Owner: lors_user
--

ALTER TABLE public.lors_complaint ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.lors_complaint_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: lors_complaintphoto; Type: TABLE; Schema: public; Owner: lors_user
--

CREATE TABLE public.lors_complaintphoto (
    id bigint NOT NULL,
    image character varying(100) NOT NULL,
    complaint_id bigint NOT NULL
);


ALTER TABLE public.lors_complaintphoto OWNER TO lors_user;

--
-- Name: lors_complaintphoto_id_seq; Type: SEQUENCE; Schema: public; Owner: lors_user
--

ALTER TABLE public.lors_complaintphoto ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.lors_complaintphoto_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: lors_review; Type: TABLE; Schema: public; Owner: lors_user
--

CREATE TABLE public.lors_review (
    id bigint NOT NULL,
    name character varying(150) NOT NULL,
    text text NOT NULL,
    photo character varying(100) NOT NULL,
    is_published boolean NOT NULL,
    created_at timestamp with time zone NOT NULL
);


ALTER TABLE public.lors_review OWNER TO lors_user;

--
-- Name: lors_review_id_seq; Type: SEQUENCE; Schema: public; Owner: lors_user
--

ALTER TABLE public.lors_review ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.lors_review_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: lors_sitesettings; Type: TABLE; Schema: public; Owner: lors_user
--

CREATE TABLE public.lors_sitesettings (
    id bigint NOT NULL,
    address character varying(500) NOT NULL,
    latitude numeric(9,6),
    longitude numeric(9,6),
    about text NOT NULL,
    instagram_url character varying(200) NOT NULL,
    telegram_url character varying(200) NOT NULL,
    whatsapp_url character varying(200) NOT NULL
);


ALTER TABLE public.lors_sitesettings OWNER TO lors_user;

--
-- Name: lors_sitesettings_id_seq; Type: SEQUENCE; Schema: public; Owner: lors_user
--

ALTER TABLE public.lors_sitesettings ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.lors_sitesettings_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Data for Name: assistant_botmessage; Type: TABLE DATA; Schema: public; Owner: lors_user
--

COPY public.assistant_botmessage (id, channel, external_user_id, direction, text, created_at) FROM stdin;
3	telegram	670765330	in	Bmw f10 2011	2026-07-19 17:15:23.915584+03
4	telegram	670765330	out	للأسف ما لقيت موديل **BMW F10 (الفئة الخامسة 5 Series)** بالكتالوج تبعنا.\n\nبس عنا موديلات تانية من BMW متوفرة، منها مثلاً:\n\n- **BMW 1 I (E87) Хэтчбек (2004–2011)** — كود الشابلون: ب-3\n- **BMW 3 (320i) (2015)** — كود الشابلون: ب-30 | النوع: تكسي عادي | الباكيج: قطعة واحدة\n- **BMW الفئة الأولى والثالثة** بموديلات تانية (E36, E46, E82, E88, F20, F21) وكمان **BMW 2 (F44)**\n\nإذا حابب نتأكد أكتر عن موديل الـ F10 أو نساعدك تختار البديل المناسب، تواصل معنا:\n\n📍 العنوان: —\n📷 Instagram: —\n✈️ Telegram: —\n💬 WhatsApp: —\n\nكنت متأكد شو الموديل بالضبط أو في تفاصيل تانية؟ خبرني ورح ساعدك 🚗	2026-07-19 17:15:35.026714+03
5	telegram	670765330	in	BMW 5 VI (F10) (2009 - 2013) NO-Xdrive	2026-07-19 17:17:17.632783+03
6	telegram	670765330	out	К сожалению, именно модели **BMW 5 VI (F10)** у нас в каталоге сейчас нет 😔\n\nНо по марке **BMW** доступны другие модели, для которых у нас есть лекала:\n\n- **BMW 1 серии I (E88)** — Кабриолет (2004–2011)\n- **BMW 1 I (E82)** — Купе (2004–2011)\n- **BMW 1 I (E87)** — Хэтчбек (2004–2011) · код шаблона: ب-3\n- **BMW 1 II (F20)** — Хэтчбек (2011–2017)\n- **BMW 1 II (F21)** — Купе (2011–2017)\n- **BMW 2 (F44)** (2019–2023)\n- **BMW 3 (320i)** (2015) · код шаблона: ب-30 · тип: обычное такси · комплектация: цельный коврик\n- **BMW 3 III (E36)** — Купе / Седан (1990–2000)\n- **BMW 3 IV (E46)** — Купе (1998–2006)\n\nЕсли у вас одна из этих моделей — с радостью подберём коврики. А если нужен именно F10 — свяжитесь с нами, возможно, мы сможем изготовить коврики по индивидуальному лекалу.\n\n📍 Адрес: —\n📷 Instagram: —\n✈️ Telegram: —\n💬 WhatsApp: —\n\nНапишите нам — поможем оформить заказ! 🚗	2026-07-19 17:17:30.802647+03
7	telegram	1283537034	in	Бмв х5	2026-07-19 17:18:04.945273+03
8	telegram	1283537034	out	Отлично, для BMW X5 у нас есть лекала под несколько поколений 👇\n\n- **BMW X5 I (E53)** — 1999–2006\n- **BMW X5 II (E70)** — 2006–2013 · код шаблона: **ب-11**\n- **BMW X5 III (F15)** — 2013–2018 · код шаблона: **ب-2**\n- **BMW X5 IV (G05)** — 2018–2023\n- **BMW X5 M II (F85)** — 2014–2018\n\nПодскажите, пожалуйста, год выпуска вашей машины — так я точно определю нужное поколение и подберу коврики по лекалам именно под вашу модель.\n\nДля оформления заказа свяжитесь с нами удобным способом:\n📍 Адрес: —\n📷 Instagram: —\n✈️ Telegram: —\n💬 WhatsApp: —	2026-07-19 17:18:14.466094+03
9	telegram	1283537034	in	2013 год	2026-07-19 17:19:00.432201+03
10	telegram	1283537034	out	Здравствуйте! Похоже, вы указали год выпуска автомобиля (2013). Чтобы я мог подобрать коврики по лекалам, подскажите, пожалуйста, **марку и модель** вашего автомобиля 🚗\n\nНапример: «Toyota Camry» или «Kia Sportage».\n\nЖду информацию — и я сразу проверю, что у нас есть для вашей машины! 😊	2026-07-19 17:19:08.740449+03
11	telegram	670765330	in	ب-38 есть же у тебя в системе	2026-07-19 17:20:06.010631+03
12	telegram	670765330	out	Извините, но у меня нет возможности искать шаблоны по коду напрямую — я подбираю коврики по марке и модели автомобиля. 🚗\n\nПодскажите, пожалуйста, марку и модель вашего авто (можно латиницей, например «Toyota Camry»), и я найду для вас подходящие шаблоны и расскажу, что есть в наличии!	2026-07-19 17:20:09.868723+03
13	telegram	1283537034	in	Бмв х5	2026-07-19 17:37:22.880624+03
14	telegram	1283537034	out	Нашёл BMW X5 в каталоге 🚗 Вот доступные поколения:\n\n| Поколение | Годы | Код шаблона |\n|---|---|---|\n| X5 I (E53) | 1999–2006 | — |\n| **X5 II (E70)** | 2006–2013 | **ب-11** |\n| **X5 III (F15)** | 2013–2018 | **ب-2** ([видео](https://www.instagram.com/reel/DUxpR96DXfO/?igsh=MTZrY3c0c3gwdzM0aQ==)) |\n| X5 IV (G05) | 2018–2023 | — |\n| X5 M II (F85) | 2014–2018 | — |\n\nГотовые лекала (коды шаблонов) есть для:\n- **X5 II (E70)** — код **ب-11**\n- **X5 III (F15)** — код **ب-2** (есть видео как выглядят коврики)\n\nПодскажите, какой у вас год выпуска — так я точно определю подходящий шаблон.\n\nДля оформления заказа свяжитесь с нами:\n📷 Instagram | ✈️ Telegram | 💬 WhatsApp	2026-07-19 17:37:31.970735+03
25	telegram	1283537034	in	Бмв х5	2026-07-19 17:46:04.091594+03
26	telegram	1283537034	out	Давайте определим ваше поколение BMW X5 — для этого мне важен **год выпуска** вашей машины 🚗\n\nПо году я сразу пойму нужное поколение и подберу код шаблона:\n\n- **2006–2013** → X5 II (E70) → код **ب-11**\n- **2013–2018** → X5 III (F15) → код **ب-2**\n\nНапишите, пожалуйста, точный год выпуска (например, «2010» или «2015») 😊	2026-07-19 17:46:08.511554+03
27	telegram	1283537034	in	2015	2026-07-19 17:46:24.842447+03
28	telegram	1283537034	out	Отлично, 2015 год — это **BMW X5 III (F15)** 🚗\n\nВот всё по вашей машине:\n- **Модель:** BMW X5 III (F15), 2013–2018\n- **Код шаблона:** **ب-2**\n- 🎥 Можете посмотреть, как выглядят наши коврики: [видео здесь](https://www.instagram.com/reel/DUxpR96DXfO/?igsh=MTZrY3c0c3gwdzM0aQ==)\n\nВсё готово для оформления заказа! Свяжитесь с нами удобным способом:\n📍 Адрес: —\n📷 Instagram: —\n✈️ Telegram: —\n💬 WhatsApp: —\n\nХотите, подскажу по вариантам комплектации или цвету? 😊	2026-07-19 17:46:29.835089+03
29	telegram	1283537034	in	Бмв х5	2026-07-19 17:48:35.216536+03
30	telegram	1283537034	out	Мы уже определили вашу машину — **BMW X5 III (F15), 2015 года** 🚗\n\nНапоминаю данные для заказа:\n- **Код шаблона:** **ب-2**\n- 🎥 [Видео с нашими ковриками](https://www.instagram.com/reel/DUxpR96DXfO/?igsh=MTZrY3c0c3gwdzM0aQ==)\n\nЕсли хотите подобрать другую машину — просто напишите марку и год 😊\nА для оформления заказа по вашему X5 свяжитесь с нами:\n📷 Instagram | ✈️ Telegram | 💬 WhatsApp	2026-07-19 17:48:39.429307+03
31	telegram	1283537034	in	2014	2026-07-19 17:48:52.669303+03
32	telegram	1283537034	out	Год 2014 для BMW X5 — это тоже **третье поколение X5 III (F15)** (выпускалось 2013–2018) 🚗\n\nДанные те же:\n- **Модель:** BMW X5 III (F15)\n- **Код шаблона:** **ب-2**\n- 🎥 [Видео с нашими ковриками](https://www.instagram.com/reel/DUxpR96DXfO/?igsh=MTZrY3c0c3gwdzM0aQ==)\n\n💡 Небольшое уточнение: в 2014 году также выпускалась спортивная версия **X5 M (F85)** — если у вас именно она, дайте знать, проверю отдельно.\n\nДля оформления заказа свяжитесь с нами:\n📷 Instagram | ✈️ Telegram | 💬 WhatsApp 😊	2026-07-19 17:48:57.802114+03
37	telegram	1283537034	in	привет, по БМВ полики	2026-07-21 17:13:40.72824+03
38	telegram	1283537034	out	Привет! 👋 Отлично, поможем с полкиами (ковриками) на BMW 🚗\n\nУточните, пожалуйста, **какая именно модель** BMW вас интересует и **год выпуска** — так я точно подберу лекала.\n\nНапример: X5, X6, 3-серия, 5-серия и т.д. 😊	2026-07-21 17:13:44.753105+03
39	telegram	1283537034	in	x6	2026-07-21 17:14:04.614659+03
40	telegram	1283537034	out	Отлично, для BMW X6 у нас есть лекала под несколько поколений 👇\n\nПодскажите, пожалуйста, **год выпуска** вашей машины — так я точно определю нужное поколение:\n- примерно **2008–2014**\n- **2014–2019**\n- **2019–2023**\n\nНапишите год — и я подберу коврики именно под вашу модель 😊	2026-07-21 17:14:35.188776+03
41	telegram	1283537034	in	2020	2026-07-21 17:14:43.508259+03
42	telegram	1283537034	out	Отлично! 2020 год — это **BMW X6 III (G06)** (поколение 2019–2023) 🚗\n\nПо вашей машине у нас есть готовые лекала: комплект идёт с цельным ковриком под водителя (с вырезом под педаль), а на втором ряду — комплект из трёх частей. Всё подгоняется точно по форме салона именно вашего X6.\n\nВсё готово для оформления заказа! Свяжитесь с нами удобным способом:\n📍 Адрес: —\n📷 Instagram: —\n✈️ Telegram: —\n💬 WhatsApp: —\n\nХотите, подскажу по цветам и материалам? 😊	2026-07-21 17:14:50.924666+03
43	telegram	1283537034	in	Есть полики на мерседес?	2026-07-22 21:37:41.315136+03
44	telegram	1283537034	out	Да, конечно! По Mercedes у нас большой выбор — есть лекала на многие модели 🚗\n\nЧтобы подобрать точно под вашу машину, подскажите, пожалуйста:\n- **какая модель** Mercedes (например A-Class, B-Class, C-Class, S-Class и т.д.)\n- **год выпуска**\n\nНапишите — и я сразу проверю, что у нас есть 😊	2026-07-22 21:37:48.5351+03
45	telegram	1283537034	in	C класс	2026-07-22 21:38:09.000233+03
46	telegram	1283537034	out	Давайте подберём коврики под ваш Mercedes C-Class 🚗\n\nДля этого поколения выпускались разные версии, поэтому уточните, пожалуйста, **год выпуска** вашей машины — так я точно определю нужное поколение и подберу лекала.\n\nНапишите примерный год (например, «2012» или «2018») 😊	2026-07-22 21:38:13.346927+03
47	telegram	1283537034	in	2016	2026-07-22 21:38:34.511705+03
48	telegram	1283537034	out	К сожалению, именно на **Mercedes C-Class 2016 года** (поколение W205) у нас пока **нет готового лекала** в каталоге 😔\n\nНо по Mercedes у нас есть готовые лекала на другие модели, например:\n- **A-Class** (2018–2025)\n- **B-Class** (2014–2018)\n\nЕсли вас интересует какая-то из них или другая модель Mercedes — напишите, я с радостью проверю 😊	2026-07-22 21:38:44.240525+03
\.


--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: lors_user
--

COPY public.auth_group (id, name) FROM stdin;
\.


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: lors_user
--

COPY public.auth_group_permissions (id, group_id, permission_id) FROM stdin;
\.


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: lors_user
--

COPY public.auth_permission (id, name, content_type_id, codename) FROM stdin;
1	Can add log entry	1	add_logentry
2	Can change log entry	1	change_logentry
3	Can delete log entry	1	delete_logentry
4	Can view log entry	1	view_logentry
5	Can add permission	3	add_permission
6	Can change permission	3	change_permission
7	Can delete permission	3	delete_permission
8	Can view permission	3	view_permission
9	Can add group	2	add_group
10	Can change group	2	change_group
11	Can delete group	2	delete_group
12	Can view group	2	view_group
13	Can add user	4	add_user
14	Can change user	4	change_user
15	Can delete user	4	delete_user
16	Can view user	4	view_user
17	Can add content type	5	add_contenttype
18	Can change content type	5	change_contenttype
19	Can delete content type	5	delete_contenttype
20	Can view content type	5	view_contenttype
21	Can add session	6	add_session
22	Can change session	6	change_session
23	Can delete session	6	delete_session
24	Can view session	6	view_session
25	Can add car model	8	add_carmodel
26	Can change car model	8	change_carmodel
27	Can delete car model	8	delete_carmodel
28	Can view car model	8	view_carmodel
29	Can add brand	7	add_brand
30	Can change brand	7	change_brand
31	Can delete brand	7	delete_brand
32	Can view brand	7	view_brand
33	Can add complaint	9	add_complaint
34	Can change complaint	9	change_complaint
35	Can delete complaint	9	delete_complaint
36	Can view complaint	9	view_complaint
37	Can add complaint photo	10	add_complaintphoto
38	Can change complaint photo	10	change_complaintphoto
39	Can delete complaint photo	10	delete_complaintphoto
40	Can view complaint photo	10	view_complaintphoto
41	Can add настройки сайта	11	add_sitesettings
42	Can change настройки сайта	11	change_sitesettings
43	Can delete настройки сайта	11	delete_sitesettings
44	Can view настройки сайта	11	view_sitesettings
45	Can add review	12	add_review
46	Can change review	12	change_review
47	Can delete review	12	delete_review
48	Can view review	12	view_review
49	Can add сообщение бота	13	add_botmessage
50	Can change сообщение бота	13	change_botmessage
51	Can delete сообщение бота	13	delete_botmessage
52	Can view сообщение бота	13	view_botmessage
\.


--
-- Data for Name: auth_user; Type: TABLE DATA; Schema: public; Owner: lors_user
--

COPY public.auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) FROM stdin;
1	pbkdf2_sha256$1200000$Ew3WWeTCH4HsCPV6vdKxtO$NKm58dhfQGn8CHTsckpQATTG53Y+nZUXvCb6bKhr97g=	2026-07-13 11:36:33.290891+03	t	halid			gracioso@pm.me	t	t	2026-07-02 18:17:56.669583+03
\.


--
-- Data for Name: auth_user_groups; Type: TABLE DATA; Schema: public; Owner: lors_user
--

COPY public.auth_user_groups (id, user_id, group_id) FROM stdin;
\.


--
-- Data for Name: auth_user_user_permissions; Type: TABLE DATA; Schema: public; Owner: lors_user
--

COPY public.auth_user_user_permissions (id, user_id, permission_id) FROM stdin;
\.


--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: lors_user
--

COPY public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
1	2026-07-13 11:00:08.476302+03	7	Usman (в работе)	2	[{"changed": {"fields": ["Status"]}}]	9	1
2	2026-07-13 11:00:14.512413+03	6	Usman (в работе)	2	[{"changed": {"fields": ["Status"]}}]	9	1
3	2026-07-13 11:01:00.753199+03	2	usman	2	[{"changed": {"fields": ["\\u041e\\u043f\\u0443\\u0431\\u043b\\u0438\\u043a\\u043e\\u0432\\u0430\\u043d"]}}]	12	1
\.


--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: lors_user
--

COPY public.django_content_type (id, app_label, model) FROM stdin;
1	admin	logentry
2	auth	group
3	auth	permission
4	auth	user
5	contenttypes	contenttype
6	sessions	session
7	lors	brand
8	lors	carmodel
9	lors	complaint
10	lors	complaintphoto
11	lors	sitesettings
12	lors	review
13	assistant	botmessage
\.


--
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: lors_user
--

COPY public.django_migrations (id, app, name, applied) FROM stdin;
1	contenttypes	0001_initial	2026-07-02 18:09:46.005256+03
2	auth	0001_initial	2026-07-02 18:09:46.053149+03
3	admin	0001_initial	2026-07-02 18:09:46.066214+03
4	admin	0002_logentry_remove_auto_add	2026-07-02 18:09:46.072536+03
5	admin	0003_logentry_add_action_flag_choices	2026-07-02 18:09:46.0927+03
6	contenttypes	0002_remove_content_type_name	2026-07-02 18:09:46.1035+03
7	auth	0002_alter_permission_name_max_length	2026-07-02 18:09:46.109062+03
8	auth	0003_alter_user_email_max_length	2026-07-02 18:09:46.112983+03
9	auth	0004_alter_user_username_opts	2026-07-02 18:09:46.117285+03
10	auth	0005_alter_user_last_login_null	2026-07-02 18:09:46.121211+03
11	auth	0006_require_contenttypes_0002	2026-07-02 18:09:46.122953+03
12	auth	0007_alter_validators_add_error_messages	2026-07-02 18:09:46.127339+03
13	auth	0008_alter_user_username_max_length	2026-07-02 18:09:46.135834+03
14	auth	0009_alter_user_last_name_max_length	2026-07-02 18:09:46.140484+03
15	auth	0010_alter_group_name_max_length	2026-07-02 18:09:46.145805+03
16	auth	0011_update_proxy_permissions	2026-07-02 18:09:46.150111+03
17	auth	0012_alter_user_first_name_max_length	2026-07-02 18:09:46.154165+03
18	sessions	0001_initial	2026-07-02 18:09:46.166316+03
19	lors	0001_initial	2026-07-02 18:27:01.020878+03
20	lors	0002_alter_carmodel_unique_together_and_more	2026-07-02 18:34:53.893084+03
21	lors	0003_complaint_complaintphoto	2026-07-12 14:18:57.036944+03
22	lors	0004_sitesettings	2026-07-12 15:18:27.284207+03
23	lors	0005_review	2026-07-12 15:26:02.027997+03
24	lors	0006_alter_brand_options_alter_carmodel_options_and_more	2026-07-13 10:12:02.472689+03
25	lors	0007_alter_carmodel_car_type_alter_carmodel_driver_cut_and_more	2026-07-13 11:16:54.153502+03
26	lors	0008_normalize_combo_choice_values	2026-07-13 11:16:54.182262+03
27	assistant	0001_initial	2026-07-19 16:39:39.936457+03
\.


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: lors_user
--

COPY public.django_session (session_key, session_data, expire_date) FROM stdin;
rj5pxumtxy4uy3l2sclgy2dys3lgszie	.eJxVjMEOwiAQRP-FsyELESwevfsNZNldpGpoUtpT479Lkx70NMnMe7OpiOtS4tpkjiOrqzLq9NslpJfUfeAn1sekaarLPCa9I_pYm75PLO_bwf4dFGyl2w7IGmHMZ0FyLhi8OE6ZZABrs00DZAsUANAlb3tCYA-cMxn03VGfL_qDOG0:1wfJCV:s1pp3qxxj8zQ_oenmLT8lEpxIcHrfCY21FZ96nLGg6Q	2026-07-16 18:19:39.828901+03
wr0unmyhibp8jnfnun2gviaw0xooed8d	.eJxVjMEOwiAQRP-FsyELESwevfsNZNldpGpoUtpT479Lkx70NMnMe7OpiOtS4tpkjiOrqzLq9NslpJfUfeAn1sekaarLPCa9I_pYm75PLO_bwf4dFGyl2w7IGmHMZ0FyLhi8OE6ZZABrs00DZAsUANAlb3tCYA-cMxn03VGfL_qDOG0:1wjApt:m4Ry4OwNJ6e_3DlT0Dqfpwb0ZjPVjZpsH4SJicbeN1o	2026-07-27 10:12:17.090665+03
7ikkpcvawfgmzz8pmcnzim3pqef0t400	.eJxVjMEOwiAQRP-FsyELESwevfsNZNldpGpoUtpT479Lkx70NMnMe7OpiOtS4tpkjiOrqzLq9NslpJfUfeAn1sekaarLPCa9I_pYm75PLO_bwf4dFGyl2w7IGmHMZ0FyLhi8OE6ZZABrs00DZAsUANAlb3tCYA-cMxn03VGfL_qDOG0:1wjC9R:MODkhPeV-XJJTIDodVMUGXG18if71zzWgxjpCYDcdsE	2026-07-27 11:36:33.291505+03
\.


--
-- Data for Name: lors_brand; Type: TABLE DATA; Schema: public; Owner: lors_user
--

COPY public.lors_brand (id, name) FROM stdin;
123	Hummer
124	Hyundai
125	haima
126	Infiniti
127	Isuzu
128	Jaecoo
129	Jaguar
130	Jeep
131	Jetour
132	Kia
133	Lamborghini
134	Lancia
135	Land Rover
136	Lexus
137	Lincoln
138	Lotus
139	Maserati
140	MG
141	Maybach
142	Mazda
143	mercedes-Benz
144	Mitsubishi
145	Nissan
146	Opel
147	Peugeot
148	Porsche
149	Renault
150	Rolls-Royce
151	Rover
152	Saab
153	SEAT
154	Skoda
155	Smart
156	SsangYong
157	Subaru
158	Suzuki
159	Tesla
160	Togg
161	Toyota
162	Volkswagen
163	Volvo
164	x peng
95	Alfa Romeo
96	Avatr
97	Audi
98	BMW
99	Bentley
100	Bugatti
101	Buick
102	BYD
103	Cadillac
104	Changan
105	Chery
106	Chevrolet
107	DFSK
108	Dacia
109	Daewoo
110	Daihatsu
111	Datsun
112	Dodge
113	fortthing
114	Fiat
115	FORD
116	FAW
117	Geely
118	Genesis
119	GMC
120	Great Wall
121	Haval
122	Honda
\.


--
-- Data for Name: lors_carmodel; Type: TABLE DATA; Schema: public; Owner: lors_user
--

COPY public.lors_carmodel (id, name, template_code, car_type, driver_cut, package, second_row_package, notes, video_url, sheet_row, brand_id) FROM stdin;
2066	Jeep Cherokee (KJ) (2001 - 2007)	ج-10	تكسي عادي	3D	لايوجد باكاج	3 قطع	تصوير السيارة كاملة		470	130
2067	Jeep Cherokee (KL) (2013 - 2023)	ج-12	خمس أبواب (هاش باك)	دعسة مقصوصة	لايوجد باكاج	3 قطع	الكليبس حديد+لايوجد شوفير+تأكيد الوارد(موجود أوربي)		471	130
2126	Kia Mohave I (HM)  (2008 - 2016) 7 مقاعد	ح-8	تكسي عادي	دعسة مقصوصة	2 قطع	قطعة واحدة	كليبس كيا + يوجد 2 باكاج		533	132
2129	Kia Optima IV (JF) (2015 - 2020)								537	132
2130	Kia Rio (2007-2011)	ح-28	تكسي عادي	دعسة مقصوصة	قطعة واحدة	3 قطع			538	132
2610	Toyota Land Cruiser J200 7 мест (2012 - 2015) Рестайлинг 1								1057	161
1857	DFSK (2025) gorly 600	س-10	تكسي عادي	دعسة مقصوصة	قطعة واحدة	قطعة واحدة	موجود سبع كراسي رجال أعمال + سبع كراسي عادي		229	107
1945	Honda CR-V V (2017 - 2021)ن	ك-14	تكسي عادي	دعسة مقصوصة			تجريب قالب على السيارة		335	122
1946	Honda CR-V (2024)	ك-5	تكسي عادي	دعسة مقصوصة	3 قطع	قطعة واحدة	سبع كراسي موجود قطعتين		336	122
1947	Honda CR-V (2026)	ك-4	تكسي عادي	دعسة مقصوصة	قطعة واحدة	قطعة واحدة	-		337	122
1948	Honda HRV I 3d Левый руль (1999 - 2006)								338	122
1949	Honda HRV I 5d Левый руль (1999 - 2006)								339	122
1999	Hyundai Santa Fe III Grand (DM) (2012 - 2018) Рестайлинг	أ-2	تكسي عادي	دعسة مقصوصة	قطعة واحدة	قطعة واحدة	تأكيد صور للصف الخلفي + صور الباكاج	https://www.instagram.com/reel/DVgmxN5DXD8/?igsh=MTU1dG5sbWpkNDg5bA==	394	124
2145	Kia Sorento II (XM) 7 мест (2013 - 2015)	ح-13	تكسي عادي	دعسة مقصوصة	2 قطع	قطعة واحدة	تصوير السيارة كاملة (تأكيد محدث او لا )		554	132
2146	Kia Sorento III 5 мест (2015 - 2020)	ح-9	تكسي عادي	دعسة مقصوصة	قطعة واحدة	قطعة واحدة	صورة الباكاج موجود سبع مقاعد	https://www.instagram.com/reel/DVlzIQ_jWTP/?igsh=MWVvaDd6OWUyeGhwbA==	555	132
2187	Land Rover defender (2023)	ل-9	تكسي عادي	دعسة مقصوصة	قطعة واحدة	قطعة واحدة	كليبس av		602	135
2227	MG - 5GL (2025)	س-1	تكسي عادي	دعسة مقصوصة	قطعة واحدة	3 قطع			647	140
2260	Mazda CX-9 I 7 мест (2006 - 2016)								682	142
2271	mercedes-Benz Actros (MP2, MP3) (2002 - 2019) Передние коврики								694	143
2280	mercedes-Benz B-Класс II (W246) рестайлинг (2014-2018)	م-15	تكسي عادي	دعسة مقصوصة	قطعة واحدة	3 قطع	موجود باكاجين اطلب صورة باكاج واضحة		703	143
2331	mercedes-Benz GLB-Class I (X247) 5 мест (2019 - 2023)	م-19	تكسي عادي	دعسة مقصوصة	قطعة واحدة	3 قطع	موجود باكاجين		756	143
2337	mercedes-Benz GLE-Class IV (x167) (2019 - 2023)	م-23	تكسي عادي	دعسة مقصوصة	قطعة واحدة	3 قطع	تأكيد تصوير كامل		762	143
2388	Mitsubishi L200 V Рестайлинг 2018-2023	ش-2	بيك آب	دعسة مقصوصة	لايوجد باكاج	3 قطع	يلزق جيرد + تأكيد صور		817	144
2397	Mitsubishi Outlander III 2012-2015 7 мест								826	144
2400	Mitsubishi Outlander (2025-2026) sport	ش-6	تكسي عادي	دعسة مقصوصة	أربع قطع	3 قطع	موجود قصتين للصالون الخلفي + الكليبس توغ + الباكاج موجود 7 مقاعد و عادي		829	144
2466	Nissan Skyline GT-R (R35) (2016-2022)								896	145
2468	Nissan Teana I (J31) Левый руль (2003 - 2008)								898	145
2477	peugeot 3008 2024-202.. (hybrid+benzin)	ك-7	تكسي عادي	دعسة مقصوصة	قطعة واحدة	قطعة واحدة	تأكيد السيارة هايبرد أو عادي + الكليبس AV		909	147
2542	Subaru Impreza IV Рестайлинг (2014-2016)								985	157
2568	Toyota C-HR I (2016 - 2019)	ص-14	تكسي عادي	دعسة مقصوصة	قطعة واحدة	3 قطع			1015	161
2588	Toyota Corolla XII (E210) (2018 - 2023)	ص-11	تكسي عادي	دعسة مقصوصة	قطعة واحدة	قطعة واحدة	الكليبس THL	https://www.instagram.com/reel/DVL7WDsgnWx/?igsh=ZXdvZ2JnbHRkdGUy	1035	161
2611	Toyota Land Cruiser J200 7 мест (2007 - 2012)	ص-22	خمس أبواب (هاش باك)	3D	قطعة واحدة	قطعة واحدة	موجود سبع كراسي ويحتاج تصوير ومقرارنة		1058	161
1997	Hyundai Santa Fe II (2009 - 2012) Рестайлинг								391	124
1722	BMW 4 I (F33) кабриолет (2013 - 2020)	ب-19	بابين (كوبي)	دعسة مقصوصة	قطعة واحدة	3 قطع	تأكيد السيارة بابين أو أربع أبواب	https://www.instagram.com/reel/DTr4kAWjWAb/?igsh=N3EzZ2thdTE3NXA=	82	98
1950	Honda Jazz I (GD) (2001 - 2008)								340	122
1951	Hummer H2 (2002 - 2009)								342	123
1952	Hummer H3 (2005 - 2010)								343	123
1953	Hyundai ix55 (2008 - 2013)								345	124
1956	Hyundai Avante V (MD) (2010 - 2015)	أ-32	تكسي عادي	دعسة مقصوصة	قطعة واحدة	قطعة واحدة		https://www.instagram.com/reel/DVbg5iZjWp9/?igsh=ZmJrNG85ZjZqNnB2	348	124
1957	Hyundai Elantra (2015-2020)	أ-16	تكسي عادي	دعسة مقصوصة	قطعة واحدة	قطعة واحدة			349	124
1958	Hyundai Coupe II (GK) Рестайлинг (2006-2009)								350	124
1959	Hyundai Creta I Рестайлинг 1 (2020 - 2021)								351	124
1960	Hyundai Новая Creta II (SU2) (2021 - 2023)	أ-15	تكسي عادي	دعسة مقصوصة	قطعة واحدة	3 قطع			352	124
1961	Hyundai Elantra III (XD) (2000 - 2010)								353	124
1962	Hyundai Elantra IV (HD) (2006 - 2011)								354	124
1963	Hyundai Elantra V (MD) (2010 - 2016)	أ-41	تكسي عادي	دعسة مقصوصة	قطعة واحدة	3 قطع			355	124
1964	Hyundai Elantra VI (AD) (2018-2020) Рестайлинг	أ_30							358	124
1965	Hyundai Elantra VII (CN7) (2020 - ...)	أ-29	تكسي عادي	دعسة مقصوصة	قطعة واحدة	3 قطع	تأكيد تصوير الباكاج مع تصوير الكليبسات الأمامية (إدخال أوربي)		359	124
1966	Hyundai Elantra VII (CN7) (2020 - ...)		تكسي عادي	دعسة مقصوصة	قطعة واحدة	3 قطع	تأكيد صور الباكاج مع تصوير الكليبسات الأمامية (إدخال كوري)		360	124
1967	Hyundai Equus II (VI) (2009 - 2016)								361	124
1968	Hyundai Genesis l (BH) (2008 - 2013)								362	124
1969	Hyundai Genesis ll (DH) (2013 - 2016)								363	124
1970	Hyundai Genesis Coupe I (2012 - 2016) Рестайлинг								364	124
1971	Hyundai Genesis G90 I (2016-2019)								365	124
1972	Genesis G80 I (DH) (2016 - 2020)								366	124
1973	Genesis G70 I (HS) (2017 - 2021)								367	124
1974	Genesis G70 I (HS) (2017 - 2021)								368	124
1975	Genesis GV80 (2020 - 2023)								369	124
1976	Hyundai Getz (TB) 5 дверей (2002 - 2011)								370	124
1977	Hyundai Grandeur IV Седан (Рестайлинг 2005-2011)								371	124
1978	Hyundai Azera Grandeur  (2011-2016)	أ-22	تكسي عادي	دعسة مقصوصة	قطعة واحدة	3 قطع			372	124
1979	Hyundai Grandeur V (HG) (2011 - 2016)								373	124
1980	Hyundai i20 I (PB) 3 двери (2008 - 2012)								374	124
1981	Hyundai i20 I (PB) 5 дверей (2008 - 2012)								375	124
1982	Hyundai i30 I (FD) (2007 - 2012)	أ-38							376	124
1983	Hyundai i30 II (GD) (2011 - 2017)	أ-81							377	124
1984	Hyundai i30 III Рестайлинг 2 универсал (2020-2023)								378	124
1985	Hyundai ix35 (LM) (2010 - 2015)								379	124
1986	Hyundai i40 I (VF) (2011 - 2017)	أ-37	تكسي عادي	دعسة مقصوصة	قطعة واحدة	3 قطع			380	124
1987	Hyundai Matrix (FC) (2001 - 2010)								381	124
1988	رجال أعمال (7مقاعد)Hyundai max cruz (2013_2	أ-11	تكسي عادي	دعسة مقصوصة	2 قطع	3 قطع			382	124
1989	Hyundai Palisade  7 мест  رجال أعمال  (2020-2024)	أ-13	تكسي عادي	دعسة مقصوصة	3 قطع	قطعة واحدة	موجود سبع كراسي رجال أعمال		383	124
1991	Hyundai Palisade (7)مقاعد	أ-20	تكسي عادي	دعسة مقصوصة	2 قطع	قطعة واحدة	كليبس op2		385	124
1992	Hyundai Palisade (LX2) 7 мест 2026 اماراتي	أ-17	تكسي عادي	دعسة مقصوصة	3 قطع	قطعة واحدة	كليبس op2 + تصوير كامل للسيارة		386	124
1993	Starx (2005)	ا-25	باكاج طويل	دعسة مقصوصة	قطعة واحدة	2 قطع	التركيب في الورشة حصرا		387	124
1994	Hyundai Santa Cruz (2021-...)								388	124
1995	Hyundai Santa Fe I (SM) (2000 - 2005)	أ-5	تكسي عادي	دعسة مقصوصة	قطعة واحدة	قطعة واحدة			389	124
1996	Hyundai Santa Fe II (CM) (2006 - 2012) Дорестайлинг	أ-1	تكسي عادي	دعسة مقصوصة	قطعة واحدة	3 قطع	تصوير دعسة الشوفير مع التأكيد (5مقاعد-7مقاعد)		390	124
1998	Hyundai Santa Fe III (DM) 7 мест (2012 - 2018)								393	124
2000	Hyundai Santa Fe IV (TM) 5 мест (2018 - 2021)	أ-19	تكسي عادي	دعسة مقصوصة	قطعة واحدة	قطعة واحدة	كليبس حديد يلزق جرد		395	124
2001	Hyundai Santa Fe IV (TM) 7 мест (2018 - 2021)	أ-23	تكسي عادي	دعسة مقصوصة	3 قطع	قطعة واحدة	تصوير السيااارة مع التوضيح وتصوير الكليبسات		396	124
2002	Hyundai Santa Fe IV (2020-2023) Рестайлинг								397	124
2003	Hyundai Santa Fe IV Рестайлинг 2020-2023 7 мест								398	124
2004	Hyundai Solaris I (RBr) Седан (2011 - 2017)								399	124
2005	Hyundai Solaris I (RBr) Хэтчбек (2011 - 2017)غ								400	124
2192	Lexus ES VI (2015 - 2018)	ص-3	تكسي عادي	دعسة مقصوصة	قطعة واحدة	قطعة واحدة	كليبس THL+لايلزق جيرد		608	136
2007	Hyundai Solaris II Рестайлинг (2020 - 2023)								402	124
2008	Hyundai Sonata III (Y3) (1993 - 1998)								403	124
2009	Hyundai Sonata IV (EF) (2001 - 2012)								404	124
2011	Hyundai Sonata VI (YF) (2009 - 2014)	أ-12	تكسي عادي	دعسة مقصوصة	قطعة واحدة	قطعة واحدة	تصوير كامل السيارة		407	124
2012	Hyundai Sonata VI (YF) (2014 - 2019)	أ-33	تكسي عادي	دعسة مقصوصة	قطعة واحدة	قطعة واحدة			408	124
2013	Hyundai Sonata VII (LF) (2017 - 2019) Рестайлинг								409	124
2014	Hyundai Sonata VIII (DN8) (2019 - 2023)								410	124
2015	Hyundai Starex (H-1) II (TQ) (2007 - 2015) سياحي كامل	أ-3	باكاج طويل	دعسة مقصوصة	قطعة واحدة	قطعة واحدة	التركيب وأخذ الطلب  حصرااا في الورشة		412	124
2016	Hyundai Starex (H-1) II (TQ) (2015 - 2018) Рестайлинг								413	124
2017	Hyundai Starex (2026)	ا-27	باكاج طويل	دعسة مقصوصة	قطعة واحدة	قطعة واحدة	اخذ الطلب والتركيب في الورشة		414	124
2018	Hyundai Starex (2022)	ا-28	باكاج طويل	دعسة مقصوصة	قطعة واحدة	قطعة واحدة	اخذ الطلب والتركيب في الورشة		415	124
2019	Hyundai Starex (2015-2022)			دعسة من تحت					416	124
2020	Hyundai Staria (2023)	أ-39	خمس أبواب (هاش باك)	دعسة مقصوصة	قطعة واحدة	قطعة واحدة	أخذ الطلب والتركيب في الورشة حصرا		417	124
2021	Hyundai Terracan I (HP) (2004 - 2007) Рестайлинг								418	124
2022	Hyundai Terracan I 2001-2004								419	124
2023	Hyundai Tiburon II (GK) (2004 - 2009)								420	124
2024	Hyundai Trajet I (FO) (‎1999 - 2008)								421	124
2025	Hyundai Tucson chiki benzin (2015-2021)	أ-9	تكسي عادي	دعسة مقصوصة	قطعة واحدة	3 قطع			422	124
2026	Hyundai Tucson I (JM) (2004 - 2010)	أ-36	تكسي عادي	دعسة مقصوصة	قطعة واحدة	قطعة واحدة	الصف الثاني نفس الصف الثاني بالسبورتاج دمعة (ورشة)		423	124
2027	Hyundai Tucson 2 (2011-2014)	أ-6	تكسي عادي	دعسة مقصوصة	قطعة واحدة	3 قطع	تصوير كامل		424	124
2028	Hyundai Tucson  (2015-2021)	أ-7	تكسي عادي	دعسة مقصوصة	قطعة واحدة	قطعة واحدة	تصوير كامل		425	124
2029	Hyundai Tucson III (TL) (2015 - 2020)	أ-40	تكسي عادي	دعسة مقصوصة	قطعة واحدة	قطعة واحدة			426	124
2030	Hyundai Tucson IV (NX4) (2020 - 2026)	أ-4	تكسي عادي	دعسة مقصوصة	قطعة واحدة	3 قطع	التأكد ان السيارة ليست توسان لاين + تصوير الصف الخلفي		427	124
2031	Hyundai Tucson IV  (2022 - 2025) n-lin	أ-14	تكسي عادي	دعسة مقصوصة	قطعة واحدة	3 قطع			428	124
2032	Hyundai Tucson (2020-2023)	أ-18	تكسي عادي	دعسة مقصوصة	قطعة واحدة	3 قطع	لايوجد دعسة شوفير لانها من نفس قالب أ-4		429	124
2033	Hyundai Veloster I (FS) (2011 - 2015)	أ-71	تكسي عادي	دعسة مقصوصة	قطعة واحدة	قطعة واحدة	تصوير من الداخل		430	124
2034	Hyundai ver crus2008-2015	أ-10	تكسي عادي	دعسة مقصوصة	قطعة واحدة	3 قطع			431	124
2035	Hyundai Veloster I Рестайлинг (2015 - 2017)								432	124
2036	Hyundai kona (2025)	أ-34	تكسي عادي	دعسة مقصوصة	قطعة واحدة	3 قطع			433	124
2037	Infiniti EX I (2007 - 2013)								437	126
2038	Infiniti FX35 I (2002 - 2009)								438	126
2039	Infiniti FX35 II (2009 - 2017)								439	126
2040	Infiniti FX37 II (2009 - 2013)	س-18	تكسي عادي	دعسة مقصوصة	لايوجد باكاج	3 قطع			440	126
2041	Infiniti FX37 II (2009 - 2013)								441	126
2042	Infiniti FX37 II (2009 - 2013)								442	126
2043	Infiniti FX37 II (2009 - 2013)								443	126
2044	Infiniti FX37 II (2009 - 2013)								444	126
2045	Infiniti M IV (2010 - 2013)								445	126
2046	Infiniti Q50 (2013 - 2017)								446	126
2047	Infiniti Q60 II Купе (2016 - 2023)								447	126
2048	Infiniti I Q70 седан (2012 - 2014)								448	126
2049	Infiniti QX80 5 мест (2013 - 2017)								449	126
2051	Infiniti QX80 I Рестайлинг 2 (2017-2020)								451	126
2052	Infiniti QX50 (2015 - 2018)								452	126
2053	Infiniti QX50 II (2017 - 2023)								453	126
2054	Infiniti QX55 (2021-2022)								454	126
2055	Infiniti QX56 5 мест (2010 - 2013)								455	126
2056	Infiniti QX56 7 мест (2010 - 2013)								456	126
2057	Infiniti QX60 I 5 мест (2013 - 2016)								457	126
2058	Infiniti QX60 I 7 мест (2013 - 2016)								458	126
2059	Infiniti QX60 I 5 мест (2016 - 2020)								459	126
2060	Infiniti QX60 I США 7 мест (2016 - 2020)								460	126
2061	Isuzu D-Max II 2012-2018								462	127
2062	Jaecoo J7 2023 - ...								464	128
2063	Jaguar xf ( 2007-2011)	ج-16	تكسي عادي	دعسة مقصوصة	لايوجد باكاج	3 قطع	لايوجد باكاج		466	129
2064	Jaguar xf (2013)	ج-21	تكسي عادي	دعسة مقصوصة	قطعة واحدة	3 قطع	الكليبس جنكل		467	129
2065	Jeep Cherokee (XJ) (1984 - 1997)								469	130
2077	eep Grand Cherokee 2 Рестайлинг (WK2) (2018 - 2023)								481	130
2068	Jeep Cherokee (KL) 2018-2023 Рестайлинг								472	130
2069	Jeep Commander 7 мест (2005-2010)								473	130
2070	Jeep Compass (2006 - 2010)								474	130
2071	Jeep Compass II (2017 - 2023)								475	130
2072	Jeep Grand Cherokee (ZJ) (1992 - 1996)								476	130
2073	Jeep Grand Cherokee (WJ) (1999 - 2004)								477	130
2074	Jeep Grand Cherokee (Wk) (2004 - 2010)								478	130
2075	Jeep Grand Cherokee (Wk2) (2010 - 2013)								479	130
2076	Jeep Grand Cherokee 1 Рестайлинг (WK2) ( 2018)	ج-20	ثلاث أبواب (هاش باك)	3D	قطعة واحدة	قطعة واحدة			480	130
2078	Jeep Grand Cherokee V (WL) (2021 - 2023) من								482	130
2079	Jeep Renegade I рестайлинг (2018 - 2023)								483	130
2080	Jeep Renegade Limited 4WD (2014 - 2020)								484	130
2081	Jeep Wrangler III (JK) 3 двери (2007 - 2018)								485	130
2082	Jeep Wrangler III (JK) 5 дверей (2006 - 2017)								486	130
2083	Jeep Wrangler Sport (JL) (2018 - 2023)								487	130
2084	Jeep Wrangler (JL) 3 двери (2017 -2023 )								488	130
2085	Jetour Dashing 2022 - ...								490	131
2086	Jetour T2 ( 2023 - ... )	س-6	تكسي عادي	دعسة مقصوصة	قطعة واحدة	قطعة واحدة	كليبس AV		491	131
2087	Jetour X70 PLUS 2020-2023								492	131
2088	Jetour X90 PLUS 2021 - ...								493	131
2089	Kia Bongo III (2004 - 2005)								495	132
2090	Kia Carens II (UN) (2006 - 2012)								496	132
2091	Kia Carnival I (KV-Ⅱ) (1998 - 2006)								497	132
2092	Kia Carnival II (VQ) (2006 - 2014)								498	132
2093	Kia Carnival II (VQ) 7 мест (2006 - 2014)								499	132
2094	Kia Carnival III (YP) (2014 - 2021)	ح-3	باكاج طويل	دعسة مقصوصة	قطعة واحدة	3 قطع	التركيب  القالب في الورشة للتأكيد		500	132
2095	Kia Carnival IV 8 мест (2020-2022)								501	132
2096	Kia Carnival IV 7 мест (2023)	ح-32	باكاج طويل	دعسة مقصوصة	قطعة واحدة	3 قطع	التفصيل والطلب في الورشة حصرااا		502	132
2097	Kia Ceed I (ED) Купе (2006 - 2012)								503	132
2098	Kia Ceed I (ED) Универсал (2006 - 2012)								504	132
2099	Kia Ceed I (ED) Хэтчбек (2006 - 2012)								505	132
2100	Kia Ceed II (JD) купе (2012-2018)								506	132
2101	Kia Ceed II (JD) Универсал (2012 - 2018)								507	132
2102	Kia Ceed II (JD) Хэтчбек (2012 - 2018)								508	132
2103	Kia Ceed III (CD) Универсал (2018 - 2021)								509	132
2104	Kia Ceed III (CD) Хэтчбек (2018 - 2021)								510	132
2105	Kia Cerato Coupe (Forte) II (TD) (2008 - 2013)	ح-16	بابين (كوبي)	دعسة مقصوصة	لايوجد باكاج	2 قطع			511	132
2106	Kia Cerato Coupe II (TD) (2008 - 2013)								512	132
2107	Kia Cerato Coupe III (YD) (2013 - 2018)								513	132
2108	Kia Cerato I (LD) (2003 - 2008)								514	132
2109	Kia Cerato II (TD) (2008 - 2013)								515	132
2110	Kia Cerato III (YD) Седан (2013 - 2018)								516	132
2111	Kia Cerato IV (BD) (2018 - 2021)								517	132
2112	Kia Cerato (2013-2018) k3	ح-25	تكسي عادي	دعسة مقصوصة	قطعة واحدة	قطعة واحدة	يلزق جيرد		518	132
2113	kia forte coupe (2008-2016)	ح-16	بابين (كوبي)	دعسة مقصوصة	لايوجد باكاج	2 قطع			519	132
2114	Kia K3 II (2013-2018)	ح -25	تكسي عادي	دعسة مقصوصة	قطعة واحدة	قطعة واحدة	طلب تصوير الكليبس		520	132
2115	Kia K3 II (2018-2021)	ح-19	تكسي عادي	دعسة مقصوصة	قطعة واحدة	3 قطع	تصوير كليبس		521	132
2116	Kia K3 II (2021-2025)	ح-26	تكسي عادي	دعسة مقصوصة	قطعة واحدة	قطعة واحدة	تأكيد يلزق جيرد+موجود كليبس؟		522	132
2117	Kia K5 (2010-2015)	ح-31	تكسي عادي	دعسة مقصوصة	قطعة واحدة	قطعة واحدة			523	132
2118	Kia K5 (2016- 2020)	ح-11	تكسي عادي	دعسة مقصوصة	قطعة واحدة	3 قطع	لايلزق الجيرد		524	132
2119	Kia K8 2021 - 2024								526	132
2120	Kia K9II (2018-2022)	ح-15	تكسي عادي	دعسة مقصوصة	قطعة واحدة	3 قطع	لايلزق الجيرد		527	132
2121	Kia K7 (العادي (2016-2021	ح-18	تكسي عادي	دعسة مقصوصة	2 قطع	3 قطع	تأكيد نوع السيارة هايبرد أو عادي وتصوير كامل		528	132
2122	Kia Magentis I Рестайлинг (2003 - 2006)								529	132
2123	Kia Magentis II Рестайлинг (2008 - 2010)								530	132
2124	Kia K7 hybrid II (2014-2021)	ح-20	تكسي عادي	دعسة مقصوصة	قطعة واحدة	3 قطع			531	132
2125	Kia Mohave I (HM) (2008 - 2016)								532	132
2127	Kia Mohave I Рестайлинг 2 2018-2023 7 мест(رجال أعمال)	ح-12	تكسي عادي	دعسة مقصوصة	3 قطع	قطعة واحدة	لايلزق الجيرد		534	132
2128	Kia Niro I 2016-2019								536	132
2152	Kia Sorento Prime III (UM) 7 мест (2014 - 2020)								561	132
2131	KIA Picanto I (SA) (2004 - 2011)	ح-29	تكسي عادي	دعسة مقصوصة	قطعة واحدة	قطعة واحدة			539	132
2132	KIA Picanto II (TA) (2011 - 2017)								540	132
2133	KIA Picanto III (JA) (2017 - 2021)								541	132
2134	Kia Pride III UB (2011-2017)								542	132
2135	Kia Quoris I (KH) (2013 - 2018)								543	132
2136	Kia Rio I (DC) Седан (1999 - 2005)								544	132
2137	Kia Rio II (JB) Седан (2005 - 2011)	ح-21	تكسي عادي	دعسة مقصوصة	قطعة واحدة	قطعة واحدة			545	132
2138	Kia Sedona III 5 мест (2014-2021)								546	132
2139	Kia Sedona III 7 мест (2014-2021)								547	132
2140	Kia Seltos (2019 - 2025)	ح-5	تكسي عادي	دعسة مقصوصة	2 قطع	3 قطع			548	132
2141	Kia Sorento I (BL) (2002 - 2010)								550	132
2142	Kia Sorento II (XM) (2009 - 2012)								551	132
2143	Kia Sorento II (XM) (2012 - 2021) Рестайлинг								552	132
2144	Kia Sorento II (XM) 7 мест (2010- 2012)	ح-23	تكسي عادي	دعسة مقصوصة	قطعة واحدة	قطعة واحدة	موجود 7 كراسي		553	132
2147	Kia Sorento III 7 мест (2014 - 2020)								556	132
2148	Kia Sorento IV 5 мест (MQ4) (2020 - 2023)								557	132
2149	Kia Sorento IV 6 мест (2020-2023)								558	132
2150	Kia Sorento IV 7 мест (MQ4) (2020 - 2023)								559	132
2151	Kia Sorento 2023-2026	ح-4	تكسي عادي	دعسة مقصوصة	قطعة واحدة	3 قطع			560	132
2153	Kia Sorento hybrid (2021-2023)*/	ح-17	تكسي عادي	دعسة مقصوصة	3 قطع	قطعة واحدة	تصوير السيارة كامل		562	132
2154	Kia Soul II (PS) (2011 - 2019)	ح-27	تكسي عادي	دعسة مقصوصة	قطعة واحدة	قطعة واحدة	تأكيد صورمع الموديل		563	132
2155	Kia Soul III (SK3) (2019 - 2023)								564	132
2156	Kia Sportage I (NB-7) (1998 - 2006)								565	132
2157	Kia Sportage II (KM) (2004 - 2009) محدث	ح- 14	تكسي عادي	دعسة مقصوصة	قطعة واحدة	قطعة واحدة	تصوير كليبس		566	132
2158	Kia Sportage II (KM) (2008 - 2010) Рестайлинг								567	132
2159	Kia Sportage III (SL) (2010 - 2016)خ	ح-7	تكسي عادي	دعسة من تحت	قطعة واحدة	قطعة واحدة	طلب تصوير الكليبس		568	132
2160	Kia Sportage IV (QL) (2016-2018)								569	132
2161	Kia Sportage (2018-2021)	ح-2	تكسي عادي	دعسة مقصوصة	قطعة واحدة	3 قطع	استشارة مسؤوال الورشة قبل تثبيت الطلب		570	132
2162	Kia Sportage V (2021 - 2023)	ح-10	تكسي عادي	دعسة مقصوصة	قطعة واحدة	قطعة واحدة	الكليبسop2 ولا يلزق الجيرد		571	132
2163	Kia Sportage  (2022-2025)	ح-6	تكسي عادي	دعسة مقصوصة	قطعة واحدة	3 قطع	تصوير واضح للدعسة الخلفية بشكل كامل		572	132
2164	Kia Sportage  (2025)	ح-30	تكسي عادي	دعسة مقصوصة	قطعة واحدة	3 قطع	وارد سلوفاكيا		573	132
2165	Kia Venga (YN) (2009 - 2014)								575	132
2166	Kia XCeed III (2020 - 2023)								576	132
2167	Kia Stinger (CK) (2017 - 2021)								577	132
2168	LADA (ВАЗ)								578	132
2169	Land Rover Defender 5d (1988 - 2016)								582	135
2170	Land Rover Defender 110 II 5d (2019 - 2023)								583	135
2171	Land Rover Discovery III (2004 - 2009)								585	135
2172	Land Rover Discovery IV (2009 - 2016)								586	135
2173	Land Rover Discovery Sport (2013 - 2016)								587	135
2174	Land Rover Discovery V (2016 - 2020)	(ل-4	تكسي عادي	دعسة مقصوصة	قطعة واحدة	قطعة واحدة + 3 قطع	تصوير السيارة		588	135
2175	Land Rover Range Rover Evoque 5d (2011 - 2019)	ل-7	تكسي عادي	دعسة مقصوصة	قطعة واحدة	3 قطع	موجود خلفيات بكليبسات وبدون كليبسات		589	135
2176	Land Rover Range Rover Evoque 5d (2019 - 2023)								590	135
2177	Land Rover Range Rover Evoque 5d (2023 - 20..)	ل-3	تكسي عادي	دعسة مقصوصة	قطعة واحدة	قطعة واحدة	موجود باكاجين + تصوير السيارة كاملة		591	135
2178	Land Rover Freelander I 1997-2003								592	135
2179	Land Rover Freelander II (2006 - 2014)								593	135
2180	Land Rover Range Rover III (2002 - 2012)								594	135
2181	Land Rover Range Rover IV (2012 -2017)								595	135
2182	Land Rover Range Rover PHEV (2018 - 2022)								596	135
2183	Land Rover Range Rover Sport I (2012)	ل-10	تكسي عادي	دعسة مقصوصة	قطعة واحدة	قطعة واحدة	تصوير وتأكيد موديل القصة		597	135
2184	Land Rover Range Rover Sport II (2016 - 2020)	ل-6	تكسي عادي	دعسة مقصوصة	قطعة واحدة	قطعة واحدة			598	135
2185	Land Rover velaar (2017-2020)	ل-2	تكسي عادي	دعسة مقصوصة	قطعة واحدة	3 قطع	كليبس حديد		599	135
2186	Land Rover Range Rover VOGUE (2012 - 2021)	ل-1	تكسي عادي	دعسة مقصوصة	قطعة واحدة	قطعة واحدة	موجود باكاجين + تصوير السيارة كاملة		600	135
2300	mercedes-Benz CLS-Class II (W218, C218) (2010 - 2014)	م-5	تكسي عادي	دعسة مقصوصة	قطعة واحدة	3 قطع	موجود نوعين باكاج ونوعين خلفيات - تأكيد صور وقياسات دقيقة		724	143
2188	Lexus CT I Рестайлинг 2014-2018								604	136
2189	Lexus ES IV (2001 - 2006)								605	136
2190	Lexus ES V Рестайлинг (2009 - 2012)								606	136
2191	Lexus ES VI (2012 - 2015)								607	136
2193	Lexus ES VII (2018 - 2021)								609	136
2194	Lexus GS I (1991 - 1997)								610	136
2195	Lexus GS II (1997 - 2005)								611	136
2196	Lexus GS III (2005 - 2011)								612	136
2197	Lexus GS IV (2011 - 2018)	ص-20	خمس أبواب (هاش باك)	دعسة مقصوصة	قطعة واحدة	قطعة واحدة			613	136
2198	Lexus GX I 470 (2002 - 2009)								614	136
2199	Lexus GX II (2009 - 2013)								615	136
2200	Lexus GX II Рестайлинг (2013 - 2019)								616	136
2201	Lexus HS 250h I Рестайлинг (2013 - 2018)								617	136
2202	Lexus IS I (1998 - 2005)								618	136
2203	Lexus IS II (2005 - 2013)								619	136
2204	Lexus IS III F sport (2013 - 2017)								620	136
2205	Lexus LS II (1994 - 2000)								621	136
2206	Lexus LS III (2000 - 2006)								622	136
2207	Lexus LS IV long (2006 - 2012)								623	136
2208	Lexus LS V (2017 - 2021)								624	136
2209	Lexus LX II (1998 - 2007)								625	136
2210	Lexus LX470 (1998 - 2007)								626	136
2211	Lexus LX 570 (2007 - 2012)								627	136
2212	Lexus LX 570 III 7 мест (2007 - 2012)								628	136
2213	Lexus LX 570 Рестайлинг (2012 - 2015)								629	136
2214	Lexus LX570 (2016 - ...)								630	136
2215	Lexus NX 200 (2014 -2017)								631	136
2216	Lexus NX 300 I Рестайлинг 2017-2021								632	136
2217	Lexus NX 250 (2021 - 2023)								633	136
2218	Lexus RX I (1998 - 2003)								634	136
2219	Lexus RX II (300, 330, 350) (2003 - 2008)								635	136
2220	Lexus RX II (400h, 450h) (2003 - 2008)								636	136
2221	Lexus RX III (2009 - 2012)								637	136
2222	Lexus RX III Рестайлинг (2012 - 2015)								638	136
2223	Lexus RX IV (2015 - 2019)								639	136
2224	Lexus RX IV 7 мест (2015-2019)								640	136
2225	Lexus RX 350 V 2022-2023								641	136
2226	Lincoln Navigator II (2002 - 2006)								643	137
2228	MG  (2025)	س-9	تكسي عادي	دعسة مقصوصة	قطعة واحدة	3 قطع			648	140
2229	mg rx5 (2025)	س-28	تكسي عادي	دعسة مقصوصة	قطعة واحدة	قطعة واحدة	السيارة لايوجد فيها كليبس + تجميع صيني		649	140
2230	Mazda 2 II (DE) (2007 - 2014)								652	142
2231	Mazda 2 III (DJ) (2014 - 2019)								653	142
2232	Mazda 3 (BK) хетчбек (2003 - 2009) рестайлинг								654	142
2233	Mazda 3 (BM) хетчбек (2013- 2018)								655	142
2234	Mazda 3 (BM) (2013- 2018)								656	142
2235	Mazda 3 I (BK) (2003 - 2008)								657	142
2236	Mazda 3 II (BL) (2009 - 2013)								658	142
2237	Mazda 3 IV (BP) 2018-2023 Седан								659	142
2238	Mazda 323 V (C) 3d (1994 - 1998)								660	142
2239	Mazda 323 VI (BJ) (1998 - 2003)								661	142
2240	Mazda 5 I (CR) (2004 - 2010)								662	142
2241	Mazda 5 II (CW) 7 мест 2010-2018								663	142
2242	Mazda 6 I (GG) (2002 - 2008)								664	142
2243	Mazda 6 II (GH) (2007 - 2012)								665	142
2244	Mazda 6 III (2012 - 2015)								666	142
2245	Mazda 6 III (GJ) (2012 - 2015) Дорестайлинг								667	142
2246	Mazda 6 III (GJ) Рестайлинг (2015 - 2018)								668	142
2247	Mazda 6 III (GL) 2-й Рестайлинг (2018-2021)								669	142
2248	Mazda 626 IV (GE) (1991-1997)								670	142
2249	Mazda 626 LX (USA) (1997 - 2002)								671	142
2250	Mazda B-Series (1998 - 2006)								672	142
2251	Mazda Bt-50 (2006 - 2011)								673	142
2252	Mazda CX-3 I 2015 - ...								674	142
2253	Mazda CX-30 (2019 - 2023)								675	142
2254	Mazda CX-4 I 2016-2019								676	142
2255	Mazda CX-4 I Рестайлинг 2019 - ...								677	142
2256	Mazda CX-5 (2011 - 2017)								678	142
2257	Mazda CX-5 (2017 - 2021)								679	142
2258	Mazda CX-7 (2006 - 2012)								680	142
2259	Mazda CX-9 I (2006-2016)								681	142
2261	Mazda CX-9 II (2016-2021)								683	142
2262	Mazda CX-9 II 5 мест (2016 - 2021)								684	142
2263	Mazda CX-9 II 7 мест (2016 - 2021)								685	142
2264	Mazda MX-5 III (NC) родстер (2005-2009)								686	142
2265	Mazda Premacy (1999 - 2004)								687	142
2266	Mazda Premacy (2005 - 2010)								688	142
2267	Mazda RX-8 (2002 - 2012)								689	142
2268	Mazda Titan 1998								690	142
2269	Mazda Tribute I Левый руль (2000 - 2007)								691	142
2270	mercedes-Benz Atego 1324 (1998 - 2005)								693	143
2272	mercedes-Benz 814 Передние коврики (1991 - 1997)								695	143
2273	mercedes-Benz A-Class I (W168) (1997 - 2004)								696	143
2274	mercedes-Benz A-Class II (W169) (2008 - 2012) Рестайлинг								697	143
2275	mercedes-Benz A-Class III (W176) (2012 - 2018)								698	143
2276	mercedes-BenzA-Класс II (W169) (2004-2007)								699	143
2277	mercedes-Benz A-Class IV (W177) (2018 - 2022)								700	143
2278	mercedes-Benz A-Class IV (W177) (2018 - 2025)	م-13	تكسي عادي	دعسة مقصوصة	قطعة واحدة	3 قطع	تصوير كامل		701	143
2279	mercedes-Benz B-Class I (W245) (2005 - 2011)								702	143
2281	mercedes-Benz C-Class I (W202) (1993 - 2001)	م-4							704	143
2282	mercedes-Benz C-Class II (W203) (2000 - 2008)								705	143
2283	mercedes-Benz C-Class II (W203) 4matic (2000 - 2008)								706	143
2284	mercedes-Benz C-Class (W203) 3-дверный купе (2008-2011)								707	143
2285	mercedes-Benz C-Class III (W204) (2006 - 2015)	م-10							708	143
2286	mercedes-Benz C-Class III (W204) (2011 - 2015) Рестайлинг	م-10							709	143
2287	mercedes-Benz C-Class III (W204) Купе (2011 - 2015) Рестайлинг								710	143
2288	mercedes-Benz C-Class IV (W205) (2014 - 2018)	م-1							711	143
2289	mercedes-Benz C-Class IV (W205) (2018 - 2021) Рестайлинг								712	143
2290	mercedes-Benz C-Class IV (С205) Купе (2014 - 2018)	م-22	بابين (كوبي)	دعسة مقصوصة	قطعة واحدة	3 قطع	الباكاج موجود قصتين (تأكيد صورة باكاج )		713	143
2291	mercedes-Benz C-Class IV (С205) Купе (2018 - 2021) Рестайлинг								714	143
2292	mercedes-Benz C-Class  w206 (2022-202....)	م-24	تكسي عادي	دعسة مقصوصة	2 قطع	3 قطع	تأكيد قصة w206		715	143
2293	mercedes-BenzCL-Class II (C215) (1999 - 2006)								717	143
2294	mercedes-Benz CL-Class AMG II Купе (C216) (2006 - 2010)								718	143
2295	mercedes-Benz CLA-Class I (C117) (2013 - 2019)	م-21	تكسي عادي	دعسة مقصوصة	قطعة واحدة	3 قطع	موجود باكاجين		719	143
2296	mercedes-Benz CLA-Class II (C118) (2019 - 2023)								720	143
2297	mercedes-Benz CLK-Class I (W208, C208) (1997 - 2003)								721	143
2298	mercedes-Benz CLK-Class II (W209) (2002 - 2010)								722	143
2299	mercedes-Benz CLS-Class I (W219, C219) (2004 - 2008)	م-7	تكسي عادي	دعسة مقصوصة	قطعة واحدة	3 قطع	تأكيد كليبسات واذا السيارة LONG أوSHORT		723	143
2301	mercedes-Benz CLS-Class II (W218, C218) (2010 - 2014)								725	143
2302	mercedes-Benz CLS 400 II (C218) Рестайлинг 2014-2017								726	143
2303	mercedes-Benz CLS-Class III (C257) (2017 - 2021)								727	143
2304	mercedes-Benz E-Class (C123) Купе (1976 - 1986)								728	143
2305	mercedes-Benz E-Class (W123) Седан (1976 - 1986)								729	143
2306	mercedes-Benz E-Class I (W124) (1984 - 1995)								730	143
2307	mercedes-Benz E-Class I (W124) Универсал (1984 - 1995)								731	143
2308	mercedes-Benz E-Class II (W210) (1995 - 2003)								732	143
2309	mercedes-Benz E-Class III (S211) Универсал (2002 - 2009)								733	143
2310	mercedes-Benz E-Class IV (C207) Купе (2009 - 2016)	م-17	بابين (كوبي)	دعسة مقصوصة	قطعة واحدة	3 قطع	تأكيد صور الباكاج		735	143
2311	mercedes-Benz E-Class IV (S212) Универсал (2009 - 2016)								736	143
2312	mercedes-Benz E-Class IV (W212) Седан (2009 - 2013) Дорестайлинг	م-6							737	143
2313	mercedes-Benz E-Class IV (W212) Седан (2013 - 2016) Рестайлинг	م-6							738	143
2314	mercedes-Benz E-Class V (S213) Универсал (2016 - 2020)								739	143
2315	mercedes-Benz E-class Coupe (C238) (2019 - 2020)								740	143
2316	mercedes-Benz E-Class V (W213) Рестайлинг Седан (2021 - 2023)								741	143
2317	mercedes-Benz E-Class V (W213) Седан (2016 - 2020)	م-8							742	143
2318	mercedes-Benz EQS SUV 580 2022-...								743	143
2319	mercedes-Benz G-Class II (W463) (1990 - 2006)								744	143
2320	mercedes-Benz G-Class II (W463) (2006 - 2008) Рестайлинг 1								745	143
2321	mercedes-Benz G-Class II (W463) 3 Двери (2008 - 2012) Рестайлинг 2								746	143
2322	mercedes-Benz G-Class II (W463) (2012 - 2015) Рестайлинг 3								747	143
2323	mercedes-Benz G-Class III (W463) (2018 - 2023)								748	143
2324	mercedes-Benz G-Class (w464) (2021-2022)	م-16	خمس أبواب (هاش باك)	دعسة مقصوصة	قطعة واحدة	قطعة واحدة			749	143
2325	mercedes-Benz GL-Class I (X164) (2006 - 2012)								750	143
2326	mercedes-Benz GL-Class I (X164) 7 мест (2006 - 2012)								751	143
2327	mercedes-Benz GL-Class II (X166) (2012 - 2015)								752	143
2328	mercedes-Benz GL-Class II (X166) 7 мест (2012 - 2015)								753	143
2329	mercedes-Benz GLA-Class I (X156) (2014 - 2019)	م-3							754	143
2330	mercedes-Benz GLA (H247) (2020 - 2023)								755	143
2412	Mitsubishi PAJERO 5.NESİL 2013-202!	ش-1	تكسي عادي	دعسة مقصوصة	قطعة واحدة	قطعة واحدة	كليبسات حديد+يلزق جيرد		841	144
2332	mercedes-Benz GLC-Class I (C253) Купе (2015 - 2019)								757	143
2333	mercedes-Benz GLC-Class I (X253) (2015 - 2019) Дорестайлинг								758	143
2334	mercedes-Benz GLC-Class I Рестайлинг (C253) Купе (2019 - 2023)								759	143
2335	mercedes-Benz GLE-Class III (C292) Купе (2015 - 2019)								760	143
2336	mercedes-Benz GLE-Class III (W166) (2015 - 2019)								761	143
2338	mercedes-Benz GLE-class Coupe IV (C167) (2019 - 2023)								763	143
2339	mercedes-Benz GLK-Class (Х204) (2008 - 2015)								764	143
2340	mercedes-Benz GLS II (X166) 5 мест (2015 - 2019)	م-20	خمس أبواب (هاش باك)	دعسة مقصوصة	قطعة واحدة	قطعة واحدة	موجود سبع مقاعد		765	143
2341	mercedes-Benz GLS II (X166) 7 мест (2015 - 2019)								766	143
2342	mercedes-Benz GLS (X167) 7 мест (2020 - 2023)								767	143
2343	mercedes-Benz GLS (X167) (2020 - ...)								768	143
2344	Maybach X222 (2014 - 2020)								770	143
2345	mercedes-Benz Maybach GLS 600(2019-2022)								771	143
2346	mercedes-Benz M-Class I (W163) (1997 - 2005)								772	143
2347	mercedes-Benz M-Class II (W164) (2005 - 2011)								773	143
2348	mercedes-Benz M-Class III (W166) (2011 - 2015)	م-9							774	143
2349	mercedes-Benz R-Class 350 I (2005 - 2007)								775	143
2350	mercedes-Benz R-Class I (W251) Long 6 мест (2007 - 2010)								776	143
2351	mercedes-Benz S-Class III (W140) (1991 - 1998)	م-12	تكسي عادي	دعسة مقصوصة	لايوجد باكاج	3 قطع	تأكيد محدث أوغير محدث 1998		777	143
2352	mercedes-Benz S-Class IV (W220) (1998 - 2005)								778	143
2353	mercedes-Benz S-Class V (W221) (2005 - 2013)	م-11	تكسي عادي	دعسة مقصوصة	قطعة واحدة	3 قطع	تصةير الدعسات الخفية مع قياس العرض من قبل الزبون		779	143
2354	mercedes-Benz S-Class VI (C217) Купе (2016 - 2020)								780	143
2355	mercedes-Benz S-Class VI (W222) (2013 - 2017)	م-2							781	143
2356	mercedes-Benz S-Class VII (W223) Long (2020 - 2023)								782	143
2357	mercedes-Benz Sl-klasse V(R230) (2001-2008)								784	143
2358	mercedes-Benz SLC-класс (R172) (2016 - 2020)								785	143
2359	mercedes-Benz SLK-Class II (R171) Родстер (2004 - 2008)								786	143
2360	mercedes-Benz Sprinter I (W901) (313) (2000 - 2006) Передние коврики								787	143
2361	mercedes-Benz Sprinter II (W906) (2006 - 2012) Передние коврики								788	143
2362	mercedes-Benz Sprinter Classic I (2013 - 2018) Передние коврики								789	143
2363	mercedes-Benz Sprinter III (VS30) (2018 - 2022) Передние коврики								790	143
2364	mercedes-Benz V-Class III (W447) (2014 - ...) Два передних коврика								791	143
2365	mercedes-Benz V-Class III (W447) (2014 - 2023)								792	143
2366	mercedes-Benz Viano II (W639) (2003 - 2010) Два передних коврика								793	143
2367	mercedes-Benz Vito I (W638) (1995 - 2003)								794	143
2368	mercedes-Benz Viano II (W639) (2003 - 2010) Два передних коврика								795	143
2369	mercedes-Benz X-Class (2017 - 2020)								796	143
2370	mercedes-Benz EQS SUV 580 2022-...	م-18	خمس أبواب (هاش باك)	دعسة مقصوصة	قطعة واحدة	قطعة واحدة	السيارة كهربا (سيدان)		797	143
2371	Mini Countryman (F60) (2016 - 2020)								798	143
2372	MINI Hatch I (R50) 2000-2006								800	143
2373	Mini Hatch III (F55-F56) Рестайлинг (2018 - 2021)								801	143
2374	Mini Cooper I (R50) (2000 - 2006)								802	143
2375	Mini Clubman I (R55) (2007–2014)								803	143
2376	Mitsubishi 3000 GT II (1994-1998)								805	144
2377	Mitsubishi ASX I (2010 - 2012)								806	144
2378	Mitsubishi ASX (2025)	ش-7	تكسي عادي	دعسة مقصوصة	قطعة واحدة	3 قطع			807	144
2379	Mitsubishi Carisma (1995 - 2003) Рестайлинг								808	144
2380	Mitsubishi Colt V (1995 - 2002)								809	144
2381	Mitsubishi Colt VI (2002-2012)								810	144
2382	Mitsubishi Fuso Canter (2010-2022)								811	144
2383	Mitsubishi Galant VIII (1996 - 2006)								812	144
2384	Mitsubishi Galant IX (2004 - 2012)								813	144
2385	Mitsubishi L200 lll (2003 - 2006)								814	144
2386	Mitsubishi L200 IV (2013)	ش-9	بيك آب	دعسة مقصوصة	لايوجد باكاج	قطعة واحدة			815	144
2387	Mitsubishi L200 V (2015 - 2019)								816	144
2389	Mitsubishi L200 (2026)	ش-3	بيك آب	دعسة مقصوصة	لايوجد باكاج	3 قطع	يلزق جيرد + تأكيد صور		818	144
2390	Mitsubishi Lancer IX (2003 - 2009)	ش-4	تكسي عادي	بدون دعسة	قطعة واحدة	3 قطع			819	144
2391	Mitsubishi Lancer X (2007 - 2010)								820	144
2392	Mitsubishi Lancer X хетчбек (2007 - 2010)								821	144
2393	Mitsubishi Lancer IX универсал (2003 - 2009)								822	144
2394	Mitsubishi Outlander I (2001 - 2008)								823	144
2395	Mitsubishi Outlander XL (2006 - 2012)								824	144
2396	Mitsubishi Outlander III (2012 -2015)								825	144
2398	Mitsubishi Outlander III Рестайлинг (2014-2015)								827	144
2399	Mitsubishi Outlander III Рестайлинг 2 (2015-2018)								828	144
2401	Mitsubishi Pajero II (1990 - 2004)								830	144
2402	Mitsubishi Pajero III (1995 - 2002)								831	144
2403	Mitsubishi Pajero Sport I (Montero) I (1998 - 2008)								832	144
2404	Mitsubishi Pajero Sport I (1998 - 2008)								833	144
2405	Mitsubishi Pajero Sport II (2008 - 2017)								834	144
2406	Mitsubishi Pajero IV 3d (2006-2011)								835	144
2407	Mitsubishi Pajero IV 5d (2006-2011)								836	144
2408	Mitsubishi Pajero Pinin (1998 - 2006)								837	144
2409	Mitsubishi Pajero Sport III (2015 - 2021)								838	144
2410	Mitsubishi Pajero Sport III 2015-2021 7 мест								839	144
2411	Mitsubishi Pajero Sport III Рестайлинг (2019 - 2023)								840	144
2413	Mitsubishi Space Star (2002 - 2004)								842	144
2414	Mitsubishi Space Wagon II (1991-1998)								843	144
2415	Mitsubishi Space Wagon III (1997 - 2003)								844	144
2416	Mitsubishi eclips cross 2522	ش-5	تكسي عادي	دعسة مقصوصة	قطعة واحدة	3 قطع			845	144
2417	Mitsubishi montero (2026)	ش-8	تكسي عادي	دعسة مقصوصة	3 قطع	3 قطع	تأكيد سبورت أو عادي		846	144
2418	Nissan 350Z I Купе (2002 - 2005)								848	145
2419	Nissan Armada (2024)	ك-3	تكسي عادي	دعسة مقصوصة	قطعة واحدة	قطعة واحدة	موجود سبع كراسي + الكليبس تووغ		849	145
2420	Nissan Almera I (N15) (1995 - 2000)								850	145
2421	Nissan Almera II (N16) (2000 - 2006)								851	145
2422	Nissan Almera Tino I (V10) (2000 - 2006)								852	145
2423	Nissan Almera Classic I (B10) (2006 - 2013)								853	145
2424	Nissan Almera III (G15) (2012 - 2018)								854	145
2425	Nissan Altima III (L31) (2001-2004)								855	145
2426	Nissan Juke I (F15) (2010 - 2019)								856	145
2427	Nissan Maxima IV (A32) (1994 - 1999)								857	145
2428	Nissan Maxima V (A33) (1999 - 2006)								858	145
2429	Nissan Maxima Vll (A35) (2008 - 2014) США								859	145
2430	Nissan Micra II (K11) (1992 - 2003)								860	145
2431	Nissan Micra III (K12) (2002 - 2010)								861	145
2432	Nissan Murano I (Z50) (2002 - 2007)								862	145
2433	Nissan Murano II (Z51) (2007 - 2016)								863	145
2434	Nissan Murano III (Z52) (2014 - 2022)								864	145
2435	Nissan Navara (NP300) (2008-2015)								865	145
2436	Nissan Navara II (D40) (2004 - 2020)								866	145
2437	Nissan Note I (E11) Левый руль (2004 - 2013)								867	145
2438	Nissan Note II (E12) Левый руль (2012 - 2020) الله								868	145
2439	Nissan Pathfinder II (R50) 5 мест (1996 - 2004)								869	145
2440	Nissan Pathfinder III (R51) 5 мест (2004 - 2010) Дорестайлинг								870	145
2441	Nissan Pathfinder III (R51) 5 мест (2010 - 2014) Рестайлинг								871	145
2442	Nissan Pathfinder III (R51) 7 мест (2004 - 2010)								872	145
2443	Nissan Pathfinder III (R51) 7 мест (2010 - 2014) Рестайлинг								873	145
2444	Nissan Pathfinder IV (R52) 5 мест (2014 - 2017) Дорестайлинг								874	145
2445	Nissan Pathfinder IV (R52) 7 мест (2014 - 2017) Дорестайлинг								875	145
2446	Nissan Patrol V (Y61) 3 двери (1997 - 2004) Дорестайлинг								876	145
2447	Nissan Patrol V (Y61) 5 дверей (1997 - 2004) Дорестайлинг								877	145
2448	Nissan Patrol V (Y61) 7 мест (1997 - 2004) Дорестайлинг								878	145
2449	Nissan Patrol V (Y61) 7 мест (2004 - 2023) Рестайлинг								879	145
2450	Nissan Patrol VI (Y62) (2010 - 2014)								880	145
2451	Nissan Patrol VI (Y62) 7 мест (2010 - 2014)								881	145
2452	Nissan Patrol VI (Y62) 7 мест (2025)	ك-6	تكسي عادي	دعسة مقصوصة	3 قطع	قطعة واحدة	موجود سبع كراسي+ الكليبس toog		882	145
2453	Nissan Primastar II (X83) (2001 - 2014)								883	145
2454	Nissan Qashqai I (J10) (2006 - 2010)								884	145
2455	Nissan Qashqai I (J10+2) (2006 - 2013)								885	145
2456	Nissan Qashqai I (J10) (2010 - 2013) Рестайлинг								886	145
2457	Nissan Qashqai II дорестайл (J11) (2013 - 2019) (Сборка: Англия)								887	145
2458	Nissan Qashqai II дорестайл (J11) (2013 - 2019) (Сборка: Россия)								888	145
2459	Nissan Qashqai II Рестайлинг (J11) (2017 - 2022)								889	145
2460	nissan rogue (2014-2019)	ك-15	تكسي عادي	دعسة مقصوصة	قطعة واحدة	قطعة واحدة	الكليبس جنكل		890	145
2461	Nissan Sentra VII (B17) (2013 - 2019)								891	145
2462	Nissan Serena (C25) III Передние коврики (2005 - 2012)								892	145
2463	Nissan Serena V (C27) 2016-2019								893	145
2464	Nissan Skyline IX (R33) Седан (1993 - 1998)								894	145
2465	Nissan Skyline X (R34) Купе (1998 - 2000)								895	145
2481	Porsche 911 (2019 - 2023)								914	148
2467	Nissan Sunny IX (B15) Седан (1998 - 2004)								897	145
2469	Nissan Teana II (J32) Левый руль (2008 - 2014)								899	145
2470	Nissan Teana III (J33/L33) Левый руль (2013 - 2020)								900	145
2471	Nissan Terrano II (R20) Левый руль (1999 - 2006) Рестайлинг								901	145
2472	Nissan Terrano III (D10) Левый руль (2014 - 2022)								902	145
2473	Nissan X-Trail I (T30) (2000 - 2007)								903	145
2474	Nissan X-Trail II (T31) (2007 - 2013)								904	145
2475	Nissan X-Trail III (T32) (2013 -2019)								905	145
2476	Nissan X-Trail IV (2021-2024)								906	145
2479	Peugeot 206 2002-2009 hatchback	ك-10	تكسي عادي	3D	قطعة واحدة	3 قطع			911	147
2480	peugeot 5008 (2024)	ك-13	تكسي عادي	دعسة مقصوصة	3 قطع	قطعة واحدة			912	147
2482	Porsche Cayenne I (957) (2008 - 2010)								916	148
2483	Porsche Cayenne II (958) (2010 - 2017)	ك-8	تكسي عادي	دعسة مقصوصة	قطعة واحدة	3 قطع			917	148
2484	Porsche Cayenne II (958) (2014 - 2018) Рестайлинг								918	148
2485	Porsche Cayenne III (2017 - 2023)	ك-16	تكسي عادي	دعسة مقصوصة	قطعة واحدة	قطعة واحدة			919	148
2486	Porsche Cayenne Coupe I (2019 - 2023)								920	148
2487	Porsche Cayman I (987C) рестайлинг (2009-2012)								921	148
2488	Porsche Cayman 718 III (982) (2016 - 2023)								922	148
2489	Porsche Macan (2013 - 2018)								923	148
2490	Porsche Panamera I (2009 - 2013) Дорестайлинг								924	148
2491	Porsche Panamera I (2013 - 2016) Рестайлинг								925	148
2492	Porsche Panamera II (2016 - 2020)								926	148
2493	Renault jeep (2014)	ك-19	تكسي عادي	دعسة مقصوصة	قطعة واحدة	قطعة واحدة	يلزق شكشاك		928	149
2494	Seat Altea XL (2009 - 2015) Рестайлинг								933	153
2495	Seat Ateca I (2016-2020)								934	153
2496	Seat Cordoba II Рестайлинг (2006-2009)								935	153
2497	Seat Ibiza III рестайлинг хэтчбек (2006 - 2008)								936	153
2498	Seat Ibiza IV хэтчбэк (2008 - 2017)								937	153
2499	Seat Leon I 1999-2006								938	153
2500	Seat Leon II (1P) (2005 - 2012)								939	153
2501	Seat Leon III (5F) (2012 - 2020)								940	153
2502	SEAT Toledo III 2004-2009							ذض	941	153
2503	Skoda Karoq (2020 - 2023)								943	154
2504	Skoda Kodiaq I (2016 - 2023)								944	154
2505	Skoda Kodiaq I 7 мест (2016 - 2023)								945	154
2506	Skoda Octavia I Tour (A4, 1U) Лифтбек (2000 - 2009)								946	154
2507	Skoda Octavia II (A5, 1Z) Лифтбек (2004 - 2013)	ك-2	تكسي عادي	دعسة مقصوصة	قطعة واحدة	3 قطع			947	154
2508	Skoda Octavia II (A5, 1Z) Универсал (2009 - 2013)								948	154
2509	Skoda Octavia III (A7, 5E) Лифтбек (2013 - 2020)								949	154
2510	Skoda Octavia IV A8 Лифтбек (2020 - 2023)								950	154
2511	Skoda Rapid I (NH3) (2012 -2017)								951	154
2512	Skoda Rapid I Рестайлинг 2017-2020								952	154
2513	Skoda Rapid (2020 -2023)								953	154
2514	Skoda Roomster I (5J) (2006 - 2015)								954	154
2515	Skoda Superb I (B5, 3U) (2001 - 2008)								955	154
2516	Skoda Superb II (B6, 3T) Лифтбек (2008 - 2015)								956	154
2517	Skoda Superb III (B8, 3V) Лифтбек (2015 - 2019)								957	154
2518	Skoda Yeti I (5L) (2009 - 2014) Дорестайлинг								958	154
2519	Skoda Yeti I (5L) (2013 - 2017) Рестайлинг								959	154
2520	Ssang Yong Actyon I (2006 - 2010)								962	156
2521	Ssang Yong Actyon II (2010 - 2013)								963	156
2522	Ssang Yong Actyon Sport II (2010 - 2016)								964	156
2523	Ssang Yong Actyon Sports I (2006 - 2010)								965	156
2524	SsangYong Istana I (1995-2003)								966	156
2525	Ssang Yong Kyron I (Дорестайлинг) (2005 - 2007)								967	156
2526	Ssang Yong Kyron I (Рестайлинг) (2007 - 2015)								968	156
2527	Ssang Yong Rexton I (2001-2009)								969	156
2528	SsangYong Rexton II Y250 (2006 – 2012)								970	156
2529	SsangYong Rodius I Рестайлинг (2007 - 2013)								971	156
2530	Ssang Yong Stavic (2015 - 2019)								972	156
2531	Ssang Yong Tivoli (2015 -2019)								973	156
2532	Subaru Forester I (1997 - 2002)								975	157
2533	Subaru Forester II (2002 - 2007)								976	157
2534	Subaru Forester III (2007 - 2012)								977	157
2535	Subaru Forester IV (2012 - 2018)								978	157
2536	Subaru Forester V (2018 - 2021)								979	157
2537	Subaru Impreza I (1992 - 2000)								980	157
2538	Subaru Impreza II (2000 - 2007)								981	157
2604	Toyota Land Cruiser 70 Правый руль(1984 - 2007)								1051	161
2478	peugeot 3008 2024-202.. (hybrid+benzin)	ك-9	تكسي عادي	دعسة مقصوصة	قطعة واحدة	قطعة واحدة	القالب التركي+موجود باكاجين +تصوير السيارة للتاكد من القاالب		910	147
2539	Subaru Impreza II (1998 - 2002)								982	157
2540	Subaru Impreza II рестайлинг (2002 - 2005)								983	157
2541	Subaru Impreza III (2007 - 2014)								984	157
2543	Subaru Impreza V (2016-2022)								986	157
2544	Subaru Legacy I 1989-1994								987	157
2545	Subaru Legacy II (1993 – 1999)								988	157
2546	Subaru Legacy III (1998 - 2004)								989	157
2547	Subaru Legacy IV (2003 - 2009)								990	157
2548	Subaru Legacy V (2009 - 2014)								991	157
2549	Subaru Legacy VI (2015 - 2017)								992	157
2550	Subaru Outback II (1998 - 2004)								993	157
2551	Subaru Outback III (2003 - 2009)								994	157
2552	Subaru Outback IV (2009 - 2014)								995	157
2553	Subaru Outback V (2015 - 2018)								996	157
2554	Subaru Outback VI (2019 - 2023)								997	157
2555	Subaru WRX I (2014 - 2017)								998	157
2556	Subaru XV (2011 - 2016)								999	157
2557	Subaru XV II (2017 - 2021)								1000	157
2558	Tesla Model 3 (2017-2022)								1003	159
2559	Tesla Model S (2012 - 2016)								1004	159
2560	Tesla Model Y I 2020-2023								1005	159
2561	Tesla Model S I 2012-2016								1006	159
2562	Toyota Auris I (E150) (2006 - 2012)								1009	161
2563	Toyota Auris II (E180)  (2012 - 2016)								1010	161
2564	Toyota Avensis I (T220) Седан (1997 - 2003)								1011	161
2566	Toyota Avensis II (T250) (2003 - 2009)								1013	161
2567	Toyota Avensis III (T270) (2009 - 2015)								1014	161
2569	Toyota C-HR I Рестайлинг(2019-2022)								1016	161
2570	Toyota Camry XV10 III (1991 - 1997)								1017	161
2571	Toyota Camry XV20 IV (1996 - 2002)								1018	161
2572	Toyota Camry XV30 V (2001 - 2006)								1019	161
2573	Toyota Camry XV40 VI (2007 - 2010)								1020	161
2574	Toyota Camry XV45 VI (2009 - 2012)								1021	161
2575	Toyota Camry XV50 VII (2011 - 2014)								1022	161
2576	Toyota Camry XV55 VII (2014 - 2018)								1023	161
2577	Toyota Camry XV70 (2017 - ...)								1024	161
2578	Toyota Camry  croz IX (2022-202...)	ص-17	تكسي عادي	دعسة مقصوصة	2 قطع	3 قطع			1025	161
2579	Toyota Celica VI (T200) (1993 - 1995)								1026	161
2580	Toyota Celica VII (T230) (1999 - 2006)								1027	161
2581	Toyota Celica VII (T230)  (1999 - 2006)								1028	161
2582	Toyota Corolla VII (E100) (1991-2000)								1029	161
2583	Toyota Corolla VIII (E110)  (1995 - 2002)								1030	161
2584	Toyota Corolla IX (E120, E130) (2000 - 2007)								1031	161
2585	Toyota Corolla IX (E121) (2000 - 2007)								1032	161
2586	Toyota Corolla X (E140, E150) (2006 - 2013)								1033	161
2587	Toyota Corolla XI (E160, E170) (2012 - 2019)								1034	161
2589	Toyota Corolla cross XII (E210) 2025-202...)	ص-12	تكسي عادي	دعسة مقصوصة	قطعة واحدة	قطعة واحدة			1036	161
2590	Toyota Corolla Verso II (E120) 5 мест (2001 - 2007)								1037	161
2591	Toyota Corolla Verso II (E120) 7 мест (2001 - 2007)								1038	161
2592	Toyota fortuo 2011	ص-7	تكسي عادي	3D	قطعة واحدة	قطعة واحدة	تأكيد صور للسيارة كامل		1039	161
2594	Toyota front lander (2025)	ص-21	تكسي عادي	دعسة مقصوصة	قطعة واحدة	3 قطع			1041	161
2595	Toyota Highlander I (U20) (2001-2003)								1042	161
2596	Toyota Highlander II (XU40) (2007 - 2013)								1043	161
2597	Toyota Highlander II (XU40) 7 мест (2007 - 2013)								1044	161
2598	Toyota Highlander III (XU50) (2013 - 2019)								1045	161
2599	Toyota Highlander III (XU50) 7 мест (2013 - 2019)								1046	161
2600	Toyota Highlander IV (U70) 5 мест 2019-2023								1047	161
2601	Toyota Hilux VII (AN10, AN20, AN30) (2004 - 2015)	ص-5							1048	161
2602	Toyota Hilux VIII (AN120, AN130) (2015 - 2020)								1049	161
2603	Toyota Hilux VIII (AN120, AN130) (2020 - 2025)	ص-2	تكسي عادي	دعسة مقصوصة	لايوجد باكاج	3 قطع	السيارة بيكاب + THL + الجرد يلزق		1050	161
2605	Toyota Land Cruiser 76 (1984 - 1999)								1052	161
2606	Toyota Land Cruiser J80 Левый руль (1989 - 1997)								1053	161
2607	Toyota Land Cruiser (J78) (1999 - 2007)								1054	161
2608	Toyota Land Cruiser J100  (1998 - 2007)	ص-18	خمس أبواب (هاش باك)	دعسة مقصوصة	لايوجد باكاج	قطعة واحدة	لايوجد باكاج		1055	161
2609	Toyota Land Cruiser J200 (2009 - 2013) برادو	ص-4	تكسي عادي	دعسة مقصوصة	أربع قطع	قطعة واحدة	تصوير السيارة مع تأكيد وجود كليبس		1056	161
2565	Toyota Avensis I (T220) Универсал (1997 - 2003)								1012	161
2613	Toyota Land Cruiser J200 (2015 - 2021) Рестайлинг 2	ص-10	تكسي عادي	3D	قطعة واحدة	قطعة واحدة	تأكيد كليبسات		1060	161
2614	Toyota Land Cruiser 300 5 мест (2021 - 2023)	ص-1	تكسي عادي	3D	قطعة واحدة	قطعة واحدة	كليبس THL		1061	161
2615	Toyota Land Cruiser Prado II J90 (1996 - 2002)								1062	161
2616	Toyota Land Cruiser Prado II J95 (1996 - 2002)								1063	161
2617	Toyota Land Cruiser Prado III J120 (2002 - 2009)	ص-16	تكسي عادي	دعسة مقصوصة	قطعة واحدة	قطعة واحدة	موجود باكاجيين		1064	161
2618	Toyota Land Cruiser Prado IV J150 (2009 - 2013) Дорестайлинг								1065	161
2619	Toyota Land Cruiser Prado IV J150 (2013 - 2018) Рестайлинг 1								1066	161
2620	Toyota Land Cruiser Prado 150 Series Рестайлинг 2 (2017 - 2020)	ص-15	تكسي عادي	دعسة مقصوصة	2 قطع	قطعة واحدة			1067	161
2621	Toyota Land Cruiser Prado (2022)	ص-6	تكسي عادي	دعسة مقصوصة	قطعة واحدة	3 قطع	كليبس THL+موجود 7 كراسي		1068	161
2622	Toyota RAV 4 I (XA10) Левый руль, 5 дверей (1994 - 2000)								1069	161
2623	Toyota RAV 4 II (CA20) 3 двери (2000 - 2006)								1070	161
2624	Toyota RAV 4 II (XA20) (2000 - 2006)								1071	161
2625	Toyota RAV 4 III (XA30) (2005 - 2014)								1072	161
2626	Toyota RAV 4 IV (CA40) (2015- 2019)	ص-19	خمس أبواب (هاش باك)	دعسة مقصوصة	لايوجد باكاج	قطعة واحدة	لايوجد باكاج		1073	161
2627	Toyota RAV 4 V (CA50) (2019 -2023)								1074	161
2628	Toyota RAV 4 II (CA20) 5 дверей (2000 - 2006)								1075	161
2629	Toyota RAV 4 III (СA30) (2005 - 2014)								1076	161
2630	Toyota RAV4 I (XA10) правый руль 3 дв (1994-2000)								1077	161
2631	Toyota RAV4 V (XA50) (2018 - ...)								1078	161
2632	Toyota RAV4 (2020-202..)	ص-9	تكسي عادي	دعسة مقصوصة	قطعة واحدة	3 قطع	تأكيد الكليبسات		1079	161
2633	Toyota Tundra double cab II (XK50) (2014 - 2016)								1080	161
2634	Toyota Verso I 5 мест (2009-2012)								1081	161
2635	Toyota Verso I (AR20) 7 мест (2009 - 2012) Дорестайлинг								1082	161
2636	Toyota Verso I (AR20) (2012 - 2018) Рестайлинг								1083	161
2637	Toyota Yaris Verso (D4-D) (1999-2005)								1084	161
2638	Toyota Yaris I (XP10) (1999 - 2005)								1085	161
2639	Toyota Yaris I Рестайлинг (2003-2005)								1086	161
2640	Toyota Yaris II (XP90) (2005 - 2013)								1087	161
2641	TOYOTA VELOZ (2025) 7مقاعد	ص-13	تكسي عادي	دعسة مقصوصة	2 قطع	قطعة واحدة	كليبس THL		1088	161
2642	Volkswagen Amarok I (2010 - 2016)								1090	162
2643	Volkswagen Amarok I рестайлинг (2016 - 2020)								1091	162
2644	Volkswagen Arteon I Лифтбек (2017 - 2020)								1092	162
2645	Volkswagen Arteon I Рестайлинг (2020-...)								1093	162
2646	Volkswagen Beetle I (A4) (1997-2005)								1094	162
2647	Volkswagen Beetle II (A5) Хэтчбек (2011 - 2019)								1095	162
2648	Volkswagen Bora (A4, 1J) (1998 - 2005)								1096	162
2649	Volkswagen Bora V (2018 - ...)								1097	162
2650	Volkswagen Caddy III (2004 - 2010) Дорестайлинг								1098	162
2651	Volkswagen Caddy III (2010 - 2015) Рестайлинг								1099	162
2652	Volkswagen Caddy IV 2015-2020								1100	162
2653	Volkswagen Caddy V (2020 - 2023)								1101	162
2654	Volkswagen Crafter I Фургон (2011 - 2017)								1102	162
2655	Volkswagen Golf III (1H) (1991 - 1997)								1103	162
2656	Volkswagen Golf IV (1J) 5 дверей (1997 - 2004)								1104	162
2657	Volkswagen Golf V (1K) 3 Двери (2003 - 2009)								1105	162
2658	Volkswagen Golf V (1K) (2003 - 2013)	ف-9	تكسي عادي	دعسة مقصوصة	قطعة واحدة	2 قطع	موجود شفطين تاكيد بصور		1106	162
2659	Volkswagen Golf V plus (1K) (2004 - 2008)								1107	162
2660	Volkswagen Golf VI (5K) (2008 - 2012)								1108	162
2661	Volkswagen Golf VI plus (2009 - 2014)								1109	162
2662	Volkswagen Golf VII (5G) (2012 - 2017)	ف-4							1110	162
2663	Volkswagen Golf VII Рестайлинг (Универсал) 2017-2020								1111	162
2664	Volkswagen Golf VIII 2020-2025								1112	162
2665	Volkswagen ID.3 I Рестайлинг 2023								1113	162
2666	Volkswagen ID.4 (2020-2022)								1114	162
2667	Volkswagen ID.6 Crozz ( 2021-...)								1115	162
2668	Volkswagen Jetta II (1G) (1984 - 1992)								1116	162
2669	Volkswagen Jetta IV (1J) (1999 - 2005)								1117	162
2670	Volkswagen Jetta V (1K5) (2005 - 2011)								1118	162
2671	Volkswagen Jetta VI (5C6) (2011 - 2019)	ف-5							1119	162
2672	Volkswagen Jetta VII (2019 - 2021)								1120	162
2673	Volkswagen LT II (LT35) (1996 - 2006)								1121	162
2674	Volkswagen Lupo (1998 - 2005)								1122	162
2675	Volkswagen Passat B3 (35i) (1988 -1993)								1123	162
2676	Volkswagen Passat B4 (35i) (1993 - 1997)								1124	162
2678	Volkswagen Passat B5 plus (3BG) (2000 - 2005)								1126	162
2679	Volkswagen Passat B4 Универсал (1993 -1997)								1128	162
2680	Volkswagen Passat В5 (3B) (1996 - 2005)								1129	162
2681	Volkswagen Passat В7 (2010 - 2015) Универсал								1130	162
2682	Volkswagen Passat В7 (3C) (2010 - 2015)	ف-2							1131	162
2683	Volkswagen Passat B8 (3G) (2014 - ...)								1132	162
2684	Volkswagen Passat B8 Универсал (2014 - 2021)	ف-10	تكسي عادي	دعسة مقصوصة	قطعة واحدة	3 قطع	موجووود 2 قطعة باكاج و 2 قطعة سائق التاكيد بالصور		1133	162
2685	Volkswagen Passat B8 (2019 - ...								1134	162
2686	Volkswagen Polo V (6R) Седан (2009 - 2015) Дорестайлинг								1135	162
2687	Volkswagen Polo V (6R) Хэтчбек (2009 - 2015) Дорестайлинг								1136	162
2688	Volkswagen Polo VI (2020 - 2022)								1137	162
2689	Volkswagen Polo V (6C) (2014 - 2020) Рестайлинг								1138	162
2690	Volkswagen Scirocco III (1K8) (2008 - 2014)								1139	162
2691	Volkswagen Sharan I (7M) (1995 - 2000)								1140	162
2692	Volkswagen Sharan I Рестайлинг 2 2003-2010								1141	162
2693	Volkswagen Sharan II правый руль 7 мест (2010-2015)								1142	162
2694	Volkswagen Transporter T4 (1998 - 2003) Два передних коврика								1143	162
2695	Volkswagen Caravelle T5 (2003 - 2009) Два передних коврика								1144	162
2696	Volkswagen Multivan T5 (2003 - 2009) Два передних коврика								1145	162
2697	Volkswagen Transporter T5 (2003 - 2015) Передние коврики								1146	162
2698	Volkswagen Caravelle T5 (2020 - 2023) Два передних коврика								1147	162
2699	Volkswagen Caravelle T6 (2015 - 2020) Два передних коврика								1148	162
2700	Volkswagen Caravelle T6 (2015 - 2020) Два передних коврика								1149	162
2701	Volkswagen Multivan T6 (2015-2020)								1150	162
2702	Volkswagen Transporter T6 (2015 - 2019) Два передних коврика								1151	162
2703	Volkswagen Teramont I 7мест (2017 - 2022)	ف-7							1152	162
2704	Volkswagen Tiguan I (2007 - 2017)	ف-6							1153	162
2705	Volkswagen Tiguan II (2016 - 2024)	ف-11	تكسي عادي	دعسة مقصوصة	3 قطع	3 قطع	كليبس av		1154	162
2706	Volkswagen Touareg I (7L) (2002 - 2010)								1155	162
2707	Volkswagen Touareg (2010-2018)	ف-1							1156	162
2708	Volkswagen Touareg III (CR) (2018 - 2023)	ف-8							1157	162
2709	Volkswagen Touran I (2006 - 2014) Рестайлинг								1158	162
2710	Volvo 850 (1991 - 1996)								1160	163
2711	Volvo C30 (2006 - 2013)								1161	163
2712	Volvo FH16 III (2002 - 2012)								1162	163
2713	Volvo S40 I Рестайлинг 1999-2004								1163	163
2714	Volvo S40 II (2004 - 2012)								1164	163
2715	Volvo S60 I (2000 - 2009)								1165	163
2716	Volvo S60 II (2010 - 2018)	ك-12	تكسي عادي	دعسة مقصوصة	قطعة واحدة	3 قطع			1166	163
2717	Volvo S60 III (2018- 2023)								1167	163
2718	Volvo S70 1997-2000								1168	163
2719	Volvo XC70 II Рестайлинг(2013-2016)								1169	163
2720	Volvo S80 I (1998 - 2006)								1170	163
2721	Volvo S80 II (2006 - 2016)								1171	163
2722	Volvo S90 II (2016 - 2020)								1172	163
2723	Volvo V40 II (2012 - 2016)								1173	163
2724	Volvo V40 II Рестайлинг 2016-2019								1174	163
2725	Volvo V70 II 2000-2004								1175	163
2726	Volvo V90 Cross Country I 2016-2020								1176	163
2727	Volvo V90 Cross Country I Рестайлинг 2020-2023								1177	163
2728	Volvo XC40 (2017 -2022)								1178	163
2729	Volvo XC60 (2008 - 2017)								1179	163
2730	Volvo XC60 II (2017 - 2022)								1180	163
2731	Volvo XC70 I (2000 - 2007)								1181	163
2732	Volvo XC70 II (2007 - 2016)								1182	163
2733	Volvo XC90 I (5 мест) (2006 - 2014) Рестайлинг								1183	163
2734	Volvo XC90 I (7 мест) (2006 - 2014) Рестайлинг								1184	163
2735	Volvo XC90 II (5 мест) (2014 - 2019) Дорестайлинг								1185	163
2736	Volvo XC90 II (7 мест) (2014 - 2019) Дорестайлинг								1186	163
2737	x peng x9 (2026)	س-24	تكسي عادي	دعسة مقصوصة	قطعة واحدة	قطعة واحدة	الكليبس AV		1188	164
2593	Toyota fortuner 2025	ص-8	تكسي عادي	دعسة مقصوصة	قطعة واحدة	3 قطع	موجود سبع كراسي + تأكيد الكليبسات	https://www.instagram.com/reel/DVWQSroDanB/?igsh=aG93Y3p0bGdwaXF3	1040	161
2612	Toyota Land Cruiser J200 (2012 - 2015) Рестайлинг 1	ص-10	تكسي عادي	3D	قطعة واحدة	قطعة واحدة	تجريب القالب قبل القص		1059	161
2677	Volkswagen Passat B3 Универсал (1988 -1993)								1125	162
1652	avatr 12(2026)	س-23	تكسي عادي	دعسة مقصوصة	قطعة واحدة	قطعة واحدة			5	96
1653	avatr 11 (2026)	س-27	تكسي عادي	دعسة مقصوصة	قطعة واحدة	قطعة واحدة			6	96
1654	Audi A3 I (8L) (1996 - 2000) Дорестайлинг								9	97
1655	Audi A3 I (8L) (2000 - 2003) Рестайлинг								10	97
1656	Audi A3 II (8P) (2008 - 2013) Рестайлинг 2								11	97
1657	Audi A3 III (8V) (2016 - 2021)								12	97
1658	Audi A3 III (8V) Седан (2012 - 2016)	ت-2							13	97
1659	Audi A3 III (8V) Хэтчбек (2012 - 2016)								14	97
1660	Audi A4 I (B5, 8D) (1994 - 2001)								15	97
1661	Audi A4 II (B6, 8E) Седан (2000 - 2006)								16	97
1662	Audi A4 II (B6, 8E) Универсал (2000 - 2006)								17	97
1663	Audi A4 III (B7, 8E) (2004 - 2009)								18	97
1664	Audi A4 III (B7, 8E) Купе (2004 - 2009)								19	97
1665	Audi A4 IV (B8, 8K) Седан (2007 - 2015)	ت-7							20	97
1666	Audi A4 IV (B8, 8K) Универсал (2007 - 2015)								21	97
1667	Audi A4 V (B9, 8W) Седан (2015 - 2020)								22	97
1668	Audi A4 V (B9, 8W) Универсал (2015 - 2020)								23	97
1669	Audi A5 I (8T) Купе (2007 - 2016)								24	97
1670	Audi A5 I (8T) Лифтбек Sportback (2007 - 2016)								25	97
1671	Audi A5 II (8W) Лифтбек Sportback (2016 - 2020) Дорестайлинг Купе								26	97
1672	Audi A5 II (F5) Лифтбек Sportback (2016 - 2020) Дорестайлинг								27	97
1673	Audi A6 I (C4, 4A) Седан (1994 - 1997)								28	97
1674	Audi A6 II (C5, 4B) Седан (1997 - 2004)								29	97
1675	Audi A6 II (C5, 4B) Универсал (1997 - 2004)								30	97
1676	Audi A6 III (C6, 4F) Седан (2004 - 2011)	ت-3							31	97
1677	Audi A6 III (C6, 4F) Универсал (2004 - 2011)								32	97
1678	Audi A6 IV (C7, 4G) Седан (2011 - 2018)	ت-4							33	97
1679	Audi A6 V (C8) Седан Рестайлинг (2022 - ...)								35	97
1680	Audi A7 I (4G8) (2010 - 2018)	ت-8							36	97
1681	Audi A7 II (4K) (2018 - 2023)								37	97
1682	Audi A8 I (D2, 4D) (1994 - 2002)								39	97
1683	Audi A8 II (D3, 4E) (2002 - 2010)								40	97
1684	Audi A8 II (D3, 4E) Long (2002 - 2010)								41	97
1685	Audi A8 III (D4, 4H) (2009 - 2017)								42	97
1686	Audi A8 III (D4, 4H) Long (2009 - 2017)	ت-6					تعديل الباكاج. اطول ب10سم		43	97
1687	Audi A8 IV (D5) (2017 - 2023)	ت-10	تكسي عادي	دعسة مقصوصة	قطعة واحدة	قطعة واحدة	تأكيدالسيارة long أو short		44	97
1688	Audi A8 IV (D5) Long (2017 - 2023)								45	97
1689	Audi Q3 I (8U) (2011 - 2018)								46	97
1690	Audi Q3 II (F3) (2018 - 2020)	ت-13	تكسي عادي	دعسة مقصوصة	قطعة واحدة	3 قطع	موجود قصتين كليبس وبدون كليبس		47	97
1691	Audi Q5 I  (2008 - 2017)	ت-12	تكسي عادي	دعسة مقصوصة	قطعة واحدة	3 قطع			48	97
1692	Audi Q5 II (FY) (2017 - 2023)								49	97
1693	Audi Q7 I (4L) (2005 - 2015)	ت-1							50	97
1694	Audi Q7 II (4M) (2015 - 2019) Дорестайлинг	ت-9	تكسي عادي	دعسة مقصوصة	قطعة واحدة	3 قطع	موجود صف ثاني ب كلبسات بدون كلبسات		51	97
1695	Audi Q8 (2018 - 2023)	ت-11	تكسي عادي	دعسة مقصوصة	قطعة واحدة	3 قطع	موجود خلفيات بدون كليبس وخلفيات بكليبس التأكيد بصور		52	97
1696	Audi TT I (8N) Купе (2003 - 2006) Рестайлинг								53	97
1697	Audi TT II (8J) Купе (2006 - 2010) Дорестайлинг								54	97
1698	Audi TT III (8S) Купе (2014 - 2019) Дорестайлинг								55	97
1699	Audi TT RS (2019 - ...)								56	97
1700	Audi e-tron I (2018-...)								57	97
1701	BMW 1 I (E82) Купе (2004 - 2011)								60	98
1702	BMW 1 I (E87) Хэтчбек (2004 - 2011)	ب-3							61	98
1703	BMW 1 II (F20) Хэтчбек (2011 - 2017)								62	98
1704	BMW 1 II (F21) Купе (2011 - 2017)								63	98
1705	BMW 1 серии I (E88) Кабриолет (2004-2011)								64	98
1706	BMW 2 (F44) (2019 - 2023)								65	98
1707	BMW 3 III (E36) Купе (1990 - 2000)								66	98
1708	BMW 3 III (E36) Седан (1990 - 2000)								67	98
1709	BMW 3 IV (E46) Купе (1998 - 2006)								68	98
1651	avatr 06(2026)	س-21	تكسي عادي	دعسة مقصوصة	قطعة واحدة	قطعة واحدة			4	96
1713	BMW 3 V (E92) Купе (2005 - 2013)	ب-15	كوبي بابين	دعسة مقصوصة	قطعة واحدة	2 قطع	تأكيد xdrive 20-28		72	98
1775	BMW i3 I (I01) (2013 - 2017)								135	98
1778	BYD Tang,L (2025)	س-4	تكسي عادي	دعسة مقصوصة	3 قطع	قطعة واحدة	الباكاج 4 قطع مفصل تفصيل خاص		142	102
1730	BMW 5 VI (F10) (2009 - 2013) Дорестайлинг								90	98
1710	BMW 3 IV (E46) Седан (1998 - 2006)	ب-4							69	98
1711	BMW 3 IV (E46) Универсал (1998 - 2006)								70	98
1712	BMW 3 V (E91) Универсал (2005 - 2013)								71	98
1714	BMW 3 V (E90) (2005-2011)	ب-27	تكسي عادي	دعسة مقصوصة	قطعة واحدة	3 قطع			74	98
1715	BMW 3 VI (F30) Седан (2011 - 2019)	ب-13							75	98
1716	BMW 3 VI (F31) Универсал (2011 - 2019)								76	98
1717	BMW 3 VI (F34) GT Лифтбек (2011 - 2019)								77	98
1718	BMW 3 (320i) (2015)	ب-30	تكسي عادي	دعسة مقصوصة	قطعة واحدة	3 قطع	320i يعني غير 320 عادي تأكيد		78	98
1719	BMW 3 VII (G20) (2018 - 2022)	ب-35	تكسي عادي	دعسة مقصوصة	قطعة واحدة	3 قطع	تأكيد تصوير كامل		79	98
1720	BMW 4 (F36) Gran coupe (2013 - 2021)	ب-8							80	98
1721	BMW 4 I (F32) купе (2013 - 2020)								81	98
1723	BMW 5 II (E28) (1981 - 1988)								83	98
1724	BMW 5 III (E34) Седан (1987 - 1996)								84	98
1725	BMW 5 III (E34) Универсал (1987 - 1996)								85	98
1726	BMW 5 IV (E39) Седан (1995 - 2004)								86	98
1727	BMW 5 IV (E39) Универсал (1995 - 2004)								87	98
1728	BMW 5 V (E60) (2002 - 2010)	ب-26	تكسي عادي	دعسة مقصوصة	قطعة واحدة	3 قطع			88	98
1729	BMW 5 V (F07) (2010-2015)	ب-22	تكسي عادي	دعسة مقصوصة	2 قطع	3 قطع			89	98
1731	BMW 5 VI (F10) (2013 - 2017) makyajsiz	ب-18	تكسي عادي	دعسة مقصوصة	قطعة واحدة	3 قطع	تأكد من صورة الطبون الأمامي وصورة الطبون الكلفي ( صور الستوب)		91	98
1732	BMW 5 VI (F10) (2013 - 2017) Рестайлинг	ب-17							92	98
1733	BMW 5 VI (F11) (2009 - 2017)								93	98
1734	BMW 5 VII (G30) Седан (200)	ب-10							94	98
1735	BMW 5 VII (G31) Универсал (2017 - 2020)								95	98
1736	BMW 5 (2025)	ب-33							96	98
1737	BMW 6 II sedan (2011-2015)	ب-37							97	98
1738	BMW 6 III (F12) Кабриолет (2011 - 2017)								98	98
1739	BMW 6 III (F13) Купе (2011 - 2017)								99	98
1740	BMW 7 II (E32) (1986 - 1994)								100	98
1741	BMW 7 II (E32) Long (1986 - 1994)								101	98
1742	BMW 7 III (E38) (1994 - 2001)								102	98
1743	BMW 7 IV (E65) (2001 - 2008)	ب-29							103	98
1744	BMW 7 IV (E66) Long (2001 - 2008)	ب-5							104	98
1745	BMW 7 V (F01) (2008 - 2015)	ب-16							105	98
1746	BMW 7 V (F01) 4WD (2008 - 2015)								106	98
1747	BMW 7 V (F02) Long (2008 - 2015)	ب-6							107	98
1748	BMW 7 i (2018)	ب-34	تكسي عادي	دعسة مقصوصة	قطعة واحدة	3 قطع			108	98
1749	BMW 7 VI (G11) (2015 - 2019)	ب-9							109	98
1750	BMW 7 серии VI (G11/G12) Рестайлинг (2019 - 2023)	ب-7							110	98
1751	BMW X1 (3000e) 2023	ب-16	تكسي عادي	دعسة مقصوصة	قطعة واحدة	3 قطع			111	98
1752	BMW X1 I (E84) (2009 - 2015)								112	98
1753	BMW X1 II (F48) (2015 - 2019)								113	98
1754	BMW X1 s*drive (2022-202..)	ب-25	تكسي عادي	دعسة مقصوصة	قطعة واحدة	3 قطع	**********		114	98
1755	BMW iX1 s*drive (2022-202..) كهربا	ب-32	تكسي عادي	دعسة مقصوصة	قطعة واحدة	3 قطع	السيارة كهربا وهو الفرق بين (ب-25 و ب-32)		115	98
1756	BMW X2 (F39) (2017 - 2023)								116	98
1757	BMW X2 (2024-202...)	ب-23	تكسي عادي	دعسة مقصوصة	قطعة واحدة	3 قطع			117	98
1758	BMW X3 I (E83) (2003 - 2010)								118	98
1759	BMW X3 II (F25) (2010 - 2017)	ب-14	تكسي عادي	دعسة مقصوصة	قطعة واحدة	3 قطع	تصوير مكان الكليبسات الأساسي		119	98
1760	BMW X3 III (G01) (2017 - 2021)	ب-31	تكسي عادي	دعسة مقصوصة	قطعة واحدة	3 قطع			120	98
1761	BMW X4 I (F26) (2014 - 2018)	ب-21	تكسي عادي	دعسة مقصوصة	قطعة واحدة	3 قطع			121	98
1762	BMW X4 II (G02) (2018 - 2021)								122	98
1763	BMW X5 I (E53) (1999 - 2006)								123	98
1764	BMW X5 II (E70) (2006 - 2013)	ب-11							124	98
1765	BMW X5 III (F15) (2013 - 2018)	ب-2					https://www.instagram.com/reel/DUxpR96DXfO/?igsh=MTZrY3c0c3gwdzM0aQ==		125	98
1766	BMW X5 M II (F85) (2014 - 2018)								126	98
1767	BMW X5 IV (G05) (2018 - 2023)								127	98
1768	BMW X6  (E71) (2008-2014)	ب-28	تكسي عادي	دعسة مقصوصة	قطعة واحدة	قطعة واحدة			128	98
1769	BMW X6 II (F16) (2014 - 2019)	ب-12							129	98
1770	BMW X6 III (G06) (2019 - 2023)	ب-24	تكسي عادي	دعسة مقصوصة	قطعة واحدة	3 قطع			130	98
1771	BMW X7 x-drive  (2019-202..)	ب-30	خمس أبواب (هاش باك)	دعسة مقصوصة	2 قطع	قطعة واحدة	موجود 7 مقاعد		131	98
1772	BMW X7 I (G07) (2018 - 2023)								132	98
1773	BMW X7 I (G07) 7 мест (2018 - ...)								133	98
1774	BMW Z4 I (E85) (2002 - 2009)								134	98
1823	Chevrolet Aveo I (T200/250) (2003 - 2012)								192	106
1776	BMW i8 I Купе (2014-2017)								136	98
1777	BYD selion  2025  (06)								141	102
1779	BYD QIN 2025	س-5							143	102
1780	BYD DESTROIAR 2025 (05)	س-14	تكسي عادي	دعسة مقصوصة	قطعة واحدة	قطعة واحدة		https://www.instagram.com/reel/DVoS80Cja7V/?igsh=MTM1YXMzajNldjRvYw==	144	102
1781	BYD song'L 2025	س-12	تكسي عادي	دعسة مقصوصة	قطعة واحدة	قطعة واحدة	موجود باكاج سفلي وباكاج علوي		145	102
1782	BYD song plus 2025	س-13	تكسي عادي	دعسة مقصوصة	قطعة واحدة	قطعة واحدة	كليبس av		146	102
1783	BYD leopard-7 (2025)	س-20	تكسي عادي	دعسة مقصوصة	قطعة واحدة	قطعة واحدة	كليبس امامي حديد		148	102
1784	BYD song pro (2025)	س-22	تكسي عادي	دعسة مقصوصة	قطعة واحدة	قطعة واحدة			149	102
1785	Cadillac escalade (2000-2022) معدل	ج-4	تكسي عادي	دعسة مقصوصة	قطعة واحدة	قطعة واحدة	التركيب في الورشة حصراً+موجود 7كراسي		151	103
1786	Cadillac escalade (2000-2022)أساسي	ج-9	تكسي عادي	دعسة مقصوصة	قطعة واحدة	قطعة واحدة	التركيب في الورشة+ موجود7 كراسي		152	103
1787	Cadillac escalade (2015-2020)	ج-18	خمس أبواب (هاش باك)	3D	لايوجد باكاج	قطعة واحدة	اخذ الطلب بالورشة مع تأكيد السبع مقاعد رجال اعمال او عادي		153	103
1788	Changan Alsvin 2018 - ...								155	104
1789	Changan CS35 (2013 - 2023)								156	104
1790	Changan CS35PLUS I 2018-2023								157	104
1791	Changan CS55 (2017 - ...)								158	104
1792	Changan CS55 PLUS I (2019 - 2021)								159	104
1793	Changan CS75 I Рестайлинг (2018 - 2023)								160	104
1794	Changan CS75PLUS II 2022-2023								161	104
1795	Changan CS85COUPE 2019-...								162	104
1796	Changan CS95 I (2017 - 2019)								163	104
1797	Changan CS95 I 7 мест (2019 - ...) Рестайлинг								164	104
1798	Changan Eado Plus 2020 - ...								165	104
1799	Changan Hunter Plus 2023-...								166	104
1800	Changan Lamore 2023								167	104
1801	Changan UNI-K (2020-2023)								168	104
1802	Changan UNI-T ( 2020-2023)								169	104
1803	Changan UNI-V (2022 - ...)								170	104
1804	Chery Omoda C 5 (2022-2023)								172	105
1805	Chery Omoda S5 (2022 - ...)								173	105
1806	Chery Tiggo (T11) (2005 - 2013) Дорестайлинг								174	105
1807	Chery Tiggo (T11) I Рестайлинг (FL) (2011-2016)								175	105
1808	Chery Tiggo 2 (2017 - 2020)								176	105
1809	Chery Tiggo 2 pro (2021-2022)								177	105
1810	Chery Tiggo 3 (2014 - 2020)l								178	105
1811	Chery Tiggo 4 Рестайлинг (2018 - 2023)								179	105
1812	Chery Tiggo 5 (T21) (2014 - 2016)								180	105
1813	Chery Tiggo 07 I (2020-2026)	س-17	تكسي عادي	دعسة مقصوصة	قطعة واحدة	قطعة واحدة			181	105
1814	Chery Tiggo Pro 7 (2020 - ...)								182	105
1815	Chery Tiggo 7 Pro Max I (2022 - ...)								183	105
1816	Chery Tiggo 8 I 5 мест (2018 - 2022)								184	105
1817	Chery Tiggo 8 I 7 мест (2018 - 2022)١١								185	105
1818	Chery Tiggo 8 Pro (2021 - 2023)								186	105
1819	Chery Tiggo 8 Pro 7 мест (2021 - 2023)								187	105
1821	Chery Tiggo 8 Pro Max 7 мест (2022-...)								189	105
1822	Chery Tiggo 9 I (2024-2025)	س-11	تكسي عادي	دعسة مقصوصة	قطعة واحدة	قطعة واحدة	موجود سبع كراسي		190	105
1824	Chevrolet Aveo II (T300) (2011 - 2017)								193	106
1825	Chevrolet Blazer II (1994 - 1998)								194	106
1826	Chevrolet Camaro V Купе (2009-2013)								195	106
1827	Chevrolet Camaro VI (2015 - 2018)								196	106
1828	Chevrolet Camaro SS рестайлинг (купе) (2018 - 2023)								197	106
1829	Chevrolet Captiva I (2006 - 2011)								198	106
1830	Chevrolet Captiva 7 мест (2006 - 2011)								199	106
1831	Chevrolet Captiva Restailing (1,2,3 ) (2011 - 2018)	ج-6	تكسي عادي	3D	قطعة واحدة	قطعة واحدة	تصوير السيارة والتأكد ريستايلنج او غير ريستايلنج		200	106
1832	Chevrolet Captiva 7 мест (2011 - 2016) рестайлинг								201	106
1833	Chevrolet Captiva 7 мест (2024)	ج-14							202	106
1834	Chevrolet Cruze I (2009 - 2015)	ج-19	تكسي عادي	دعسة مقصوصة	قطعة واحدة	3 قطع	طلب تصوير دعسة الشوفير		203	106
1835	Chevrolet Cruze Хэтчбек (2009 - 2015)								205	106
1836	Chevrolet Epica I (2006 - 2012)								206	106
1837	Chevrolet Equinox (2004 - 2009)								207	106
1838	Chevrolet Equinox III (2017-2020)								208	106
1839	Chevrolet Express (1996 - 2002)								209	106
1840	Chevrolet Lacetti (2004 - 2013) седан								210	106
1841	Chevrolet Lacetti Универсал (2004 - 2013)								211	106
1842	Chevrolet Lacetti Хэтчбек (2004 - 2013)								212	106
1851	Chevrolet TrailBlazer II (2012 - 2016)								222	106
1844	Chevrolet Malibu IX (2015-2018)								214	106
1846	Chevrolet Nexia I (2017-...)								216	106
1847	Chevrolet Tahoe 840 (2000 - 2005)								217	106
1848	Chevrolet Tahoe IV 7 мест (2006 - 2014) suberban	ج-13	خمس أبواب (هاش باك)	3D	قطعة واحدة	قطعة واحدة	سبع مقاعد + ليس رجال اعمال+السيارة سوبربان		218	106
1849	Chevrolet Tahoe IV 7 мест (2014 - 2020)	ج-3	تكسي عادي	3D	قطعة واحدة	قطعة واحدة			220	106
1850	Chevrolet Tahoe(2026)	ج-22	تكسي عادي	3D	3 قطع	قطعة واحدة	سبع		221	106
1852	Chevrolet TrailBlazer III (2020-2022)								223	106
1853	Chevrolet Traverse II кроссовер 7 мест (2017 - 2021)								224	106
1854	Chevrolet SILVERADO (2021-202..)	ج-5	بيك آب	دعسة مقصوصة	لايوجد باكاج	قطعة واحدة	لايلزق الجيرد+تصوير السيارة		225	106
1855	Chevrolet SILVERADO (2017)	ج-15	بيك آب	3D	لايوجد باكاج	قطعة واحدة			226	106
1856	DFSK seres 3 (2025)	س-24	تكسي عادي	دعسة مقصوصة	قطعة واحدة	قطعة واحدة	5 مقاعد		228	107
1858	Dodge Caliber (2006 - 2011)								235	112
1859	Dodge Caravan (2000 - 2007)								236	112
1860	Dodge Challenger (2008 - 2010)								237	112
1861	Dodge Challenger III (2014 - 2023) Рестайлинг								238	112
1862	Dodge Charger VI (LX) (2015)	ج-8	تكسي عادي	دعسة مقصوصة	قطعة واحدة	قطعة واحدة			239	112
1863	Dodge Durango III (2010 - 2013)								240	112
1864	Dodge Grand Caravan V (2007-2020)								241	112
1865	Dodge Journey I Рестайлинг (2011 - 2020)								242	112
1866	Dodge Nitro (2006 - 2011)								243	112
1867	Dodge RAM III (2001-2008)								244	112
1868	Dodge RAM IV (2008 - 2018)								245	112
1869	forthing friday (reev) (2026)	س-25	تكسي عادي	دعسة مقصوصة	قطعة واحدة	قطعة واحدة			247	113
1870	forthing  S7 (reev) (2026)	س-27							248	113
1871	Ford Explorer II (1994-2003)								251	115
1872	Ford Explorer IV (U251) 5 мест (2006 - 2010)								252	115
1873	Ford Explorer IV (U251) 7 мест (2006 - 2010)								253	115
1874	Ford Explorer V (U502) (2010 - 2015) Дорестайлинг								254	115
1875	Ford Explorer V (U502) 5 мест (2015 - 2018) Рестайлинг								255	115
1876	Ford Explorer V (U502) 7 мест (2015 - 2018) Рестайлинг								256	115
1877	Ford F-150 X (1996 - 2004)								257	115
1878	Ford F-150 XI Одинарная кабина (2003 - 2008)								258	115
1879	Ford F-150 XIII 2014-2018								259	115
1880	Ford F-150 Raptor SuperCrew XIII (2017 - 2020) Рестайлинг								260	115
1881	Ford F-450 III (P473) (2011 - 2016)								261	115
1882	Ford Mustang VI (S550) (2015 - 2017)								262	115
1883	Ford Ranger ll (2006 - 2011)								263	115
1884	Ford Ranger lll (T6) (2011 - 2015)								264	115
1885	Ford Ranger IV (2015-2019)								265	115
1886	ford focus (2004-2011)	ج-23	تكسي عادي	3D	2 قطع	3 قطع			266	115
1887	Geely Atlas I (2016 - 2022)								270	117
1888	Geely Atlas II 2023 - ...								271	117
1889	Geely Coolray I (2020 - 2023)								272	117
1890	Geely Coolray I Рестайлинг 2023 - ...								273	117
1891	Geely Emgrand EC7 (2009 - 2016)								274	117
1892	Geely Emgrand 7 I 2016-2020								275	117
1893	Geely Emgrand X7 (2011 - 2016)								276	117
1894	Geely Emgrand X7 I Рестайлинг 2 (2018 - 2020)								277	117
1895	Geely Emgrand II 2021 - ...								278	117
1896	Geely FC Vision (2006-2011)								279	117
1897	Geely GC 6 (2014 - 2016)								280	117
1898	Geely Icon 2020-...								281	117
1899	Geely MK I (2006 - 2015)								282	117
1900	Geely MK Cross (2010 - 2016)								283	117
1901	Geely Monjaro 2021-2023								284	117
1902	Geely Okavango I (2020-2025)								285	117
1903	Geely Okavango I Рестайлинг (2023-2025)								286	117
1904	Geely CK (Otaka) I (2005-2008)								287	117
1905	Geely Tugella (2020 – 2023)								288	117
1907	gmc yoken denale (2016)	ج-17	خمس أبواب (هاش باك)	3D	أربع قطع	قطعة واحدة			294	119
1908	Haval Dargo (2022- ...)								297	121
1909	Haval Dargo X (2022-...)								298	121
1910	Haval F7x I (2019-2022)								299	121
1911	HAVAL F7 (2019 - 2022)								300	121
1912	Haval F7 I Рестайлинг 2022 - ...								301	121
1913	Haval F7 II (2024)								302	121
1914	HAVAL H2 (2015 - 2020)								303	121
1915	HAVAL H2 (2020 - 2021)								304	121
1916	HAVAL H5 (2020 - 2021)								305	121
1930	Honda Civic VI хетчбэк (1995 - 2000)								320	122
1931	Honda Civic VII 5 дверей (2003 - 2006) Дорестайлинг								321	122
1932	Honda Civic VII 5 дверей (2003 - 2006) Рестайлинг								322	122
1933	Honda Civic VII хетчбек 3d Левый руль (2000 - 2005)								323	122
1934	Honda Civic VII Седан 3d (2000 - 2005)								324	122
1935	Honda Civic VIII 4d (2005 - 2011)								325	122
1936	Honda Civic VIII 5d (2005 - 2011)								326	122
1937	Honda Civic X Седан 2015-2021								327	122
1938	Honda Civic X Хэтчбек 2015-2021)								328	122
1939	Honda Civic XI (2022)								329	122
1940	Honda CR-V I (АКПП) (1997 - 2001)								330	122
1941	Honda CR-V I (МКПП) (1997 - 2001)								331	122
1942	Honda CR-V II (2002 - 2006)								332	122
2050	Infiniti QX80 7 мест (2021)	س-19	تكسي عادي	دعسة مقصوصة	أربع قطع	قطعة واحدة	التأكد من الوارد (موجود كوري)		450	126
1820	Chery Tiggo 8 Pro 7 мест (2026)	س-16	خمس أبواب (هاش باك)	دعسة مقصوصة	أربع قطع	قطعة واحدة	تأكيد الوارد ( موجود الكوري)		188	105
1843	Chevrolet Lanos (2002 - 2009)								213	106
1845	Chevrolet Malibu IX (2018-2022) Рестайлинг	ج-11	تكسي عادي	دعسة مقصوصة	قطعة واحدة	قطعة واحدة	كليبس op2		215	106
1906	Genesis g80 2015	ك-1	تكسي عادي	دعسة مقصوصة	قطعة واحدة	3 قطع	تصوير كامل للسيارة ، تأكيد الكليبس		290	118
1917	HAVAL H6 (2014 - 2020)	س-3	تكسي عادي	دعسة مقصوصة	قطعة واحدة	قطعة واحدة	تصوير كامل + تأكيد الكليبس		306	121
1918	HAVAL H9 5 мест (2014 - 2017)								307	121
1919	HAVAL H9 7 мест (2014 - 2017)	س-2	تكسي عادي	دعسة مقصوصة	قطعة واحدة	قطعة واحدة	تصوير السيارة + تأكيد الكليبس		308	121
1920	Haval Jolion I (2021 - ...)								309	121
1921	Haval M6 II ( 2021 - ...)								310	121
1922	Honda Accord VI (CF/CL) (1997 - 2002)								312	122
1923	Honda Accord VII (CL) (2002 - 2008)								313	122
1924	Honda Accord VIII (CU) (2008 - 2013)								314	122
1925	Honda Accord IX (CR) (2013 - 2017)								315	122
1926	Honda Accord X 2018-2022	ك-11	تكسي عادي	دعسة مقصوصة	قطعة واحدة	3 قطع			316	122
1927	Honda Accord (2023)	ك-18	تكسي عادي	دعسة مقصوصة	قطعة واحدة	3 قطع	تصوير كامل مع قياسات عرض دقيقة		317	122
1928	Honda Civic V (1992 - 1995)								318	122
1929	Honda Civic VI седан (1995 - 2000)								319	122
1943	Honda CR-V III (2007 - 2011)								333	122
1944	Honda CR-V IV (2012 - 2016)								334	122
1954	Hyundai ix55 7 мест 2008-2013								346	124
1955	Hyundai Accent  (2011)	أ-35	تكسي عادي	دعسة مقصوصة	قطعة واحدة	قطعة واحدة	تأكيد صور لأماكن الكليبس		347	124
1990	Hyundai Palisade (LX2) 7 мест 2026 رجال أعمال	أ-24	تكسي عادي	دعسة مقصوصة	أربع قطع	قطعة واحدة	كليبس op2 + سبع مقاعد وتصوير السيارة كامل		384	124
2006	Hyundai Solaris II (HCr) (2017 - 2020)								401	124
2010	Hyundai Sonata V (NF) (2004 - 2010)	أ-42	تكسي عادي	دعسة مقصوصة	لايوجد باكاج	3 قطع	لايوجد قالب باكاج		405	124
\.


--
-- Data for Name: lors_complaint; Type: TABLE DATA; Schema: public; Owner: lors_user
--

COPY public.lors_complaint (id, name, phone, text, status, created_at, car_model_id) FROM stdin;
7	Usman	09876678876	test	in_progress	2026-07-12 15:11:40.550829+03	1654
6	Usman	09876678876	test	in_progress	2026-07-12 15:09:04.70652+03	1701
\.


--
-- Data for Name: lors_complaintphoto; Type: TABLE DATA; Schema: public; Owner: lors_user
--

COPY public.lors_complaintphoto (id, image, complaint_id) FROM stdin;
\.


--
-- Data for Name: lors_review; Type: TABLE DATA; Schema: public; Owner: lors_user
--

COPY public.lors_review (id, name, text, photo, is_published, created_at) FROM stdin;
2	usman	test	reviews/2026/07/Снимок_экрана_2026-07-11_в18.36.48.png	t	2026-07-12 15:30:02.62757+03
\.


--
-- Data for Name: lors_sitesettings; Type: TABLE DATA; Schema: public; Owner: lors_user
--

COPY public.lors_sitesettings (id, address, latitude, longitude, about, instagram_url, telegram_url, whatsapp_url) FROM stdin;
1		\N	\N				
\.


--
-- Name: assistant_botmessage_id_seq; Type: SEQUENCE SET; Schema: public; Owner: lors_user
--

SELECT pg_catalog.setval('public.assistant_botmessage_id_seq', 48, true);


--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: lors_user
--

SELECT pg_catalog.setval('public.auth_group_id_seq', 1, false);


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: lors_user
--

SELECT pg_catalog.setval('public.auth_group_permissions_id_seq', 1, false);


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: lors_user
--

SELECT pg_catalog.setval('public.auth_permission_id_seq', 52, true);


--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: lors_user
--

SELECT pg_catalog.setval('public.auth_user_groups_id_seq', 1, false);


--
-- Name: auth_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: lors_user
--

SELECT pg_catalog.setval('public.auth_user_id_seq', 1, true);


--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: lors_user
--

SELECT pg_catalog.setval('public.auth_user_user_permissions_id_seq', 1, false);


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: lors_user
--

SELECT pg_catalog.setval('public.django_admin_log_id_seq', 3, true);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: lors_user
--

SELECT pg_catalog.setval('public.django_content_type_id_seq', 13, true);


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: lors_user
--

SELECT pg_catalog.setval('public.django_migrations_id_seq', 27, true);


--
-- Name: lors_brand_id_seq; Type: SEQUENCE SET; Schema: public; Owner: lors_user
--

SELECT pg_catalog.setval('public.lors_brand_id_seq', 164, true);


--
-- Name: lors_carmodel_id_seq; Type: SEQUENCE SET; Schema: public; Owner: lors_user
--

SELECT pg_catalog.setval('public.lors_carmodel_id_seq', 2737, true);


--
-- Name: lors_complaint_id_seq; Type: SEQUENCE SET; Schema: public; Owner: lors_user
--

SELECT pg_catalog.setval('public.lors_complaint_id_seq', 7, true);


--
-- Name: lors_complaintphoto_id_seq; Type: SEQUENCE SET; Schema: public; Owner: lors_user
--

SELECT pg_catalog.setval('public.lors_complaintphoto_id_seq', 3, true);


--
-- Name: lors_review_id_seq; Type: SEQUENCE SET; Schema: public; Owner: lors_user
--

SELECT pg_catalog.setval('public.lors_review_id_seq', 2, true);


--
-- Name: lors_sitesettings_id_seq; Type: SEQUENCE SET; Schema: public; Owner: lors_user
--

SELECT pg_catalog.setval('public.lors_sitesettings_id_seq', 1, false);


--
-- Name: assistant_botmessage assistant_botmessage_pkey; Type: CONSTRAINT; Schema: public; Owner: lors_user
--

ALTER TABLE ONLY public.assistant_botmessage
    ADD CONSTRAINT assistant_botmessage_pkey PRIMARY KEY (id);


--
-- Name: auth_group auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: lors_user
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions auth_group_permissions_group_id_permission_id_0cd325b0_uniq; Type: CONSTRAINT; Schema: public; Owner: lors_user
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: lors_user
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: lors_user
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_permission auth_permission_content_type_id_codename_01ab375a_uniq; Type: CONSTRAINT; Schema: public; Owner: lors_user
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq UNIQUE (content_type_id, codename);


--
-- Name: auth_permission auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: lors_user
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups auth_user_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: lors_user
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups auth_user_groups_user_id_group_id_94350c0c_uniq; Type: CONSTRAINT; Schema: public; Owner: lors_user
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_group_id_94350c0c_uniq UNIQUE (user_id, group_id);


--
-- Name: auth_user auth_user_pkey; Type: CONSTRAINT; Schema: public; Owner: lors_user
--

ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions auth_user_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: lors_user
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions auth_user_user_permissions_user_id_permission_id_14a6b632_uniq; Type: CONSTRAINT; Schema: public; Owner: lors_user
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_permission_id_14a6b632_uniq UNIQUE (user_id, permission_id);


--
-- Name: auth_user auth_user_username_key; Type: CONSTRAINT; Schema: public; Owner: lors_user
--

ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_username_key UNIQUE (username);


--
-- Name: django_admin_log django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: lors_user
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- Name: django_content_type django_content_type_app_label_model_76bd3d3b_uniq; Type: CONSTRAINT; Schema: public; Owner: lors_user
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq UNIQUE (app_label, model);


--
-- Name: django_content_type django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: lors_user
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_migrations django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: lors_user
--

ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- Name: django_session django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: lors_user
--

ALTER TABLE ONLY public.django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: lors_brand lors_brand_name_key; Type: CONSTRAINT; Schema: public; Owner: lors_user
--

ALTER TABLE ONLY public.lors_brand
    ADD CONSTRAINT lors_brand_name_key UNIQUE (name);


--
-- Name: lors_brand lors_brand_pkey; Type: CONSTRAINT; Schema: public; Owner: lors_user
--

ALTER TABLE ONLY public.lors_brand
    ADD CONSTRAINT lors_brand_pkey PRIMARY KEY (id);


--
-- Name: lors_carmodel lors_carmodel_pkey; Type: CONSTRAINT; Schema: public; Owner: lors_user
--

ALTER TABLE ONLY public.lors_carmodel
    ADD CONSTRAINT lors_carmodel_pkey PRIMARY KEY (id);


--
-- Name: lors_carmodel lors_carmodel_sheet_row_d3a9bf9b_uniq; Type: CONSTRAINT; Schema: public; Owner: lors_user
--

ALTER TABLE ONLY public.lors_carmodel
    ADD CONSTRAINT lors_carmodel_sheet_row_d3a9bf9b_uniq UNIQUE (sheet_row);


--
-- Name: lors_complaint lors_complaint_pkey; Type: CONSTRAINT; Schema: public; Owner: lors_user
--

ALTER TABLE ONLY public.lors_complaint
    ADD CONSTRAINT lors_complaint_pkey PRIMARY KEY (id);


--
-- Name: lors_complaintphoto lors_complaintphoto_pkey; Type: CONSTRAINT; Schema: public; Owner: lors_user
--

ALTER TABLE ONLY public.lors_complaintphoto
    ADD CONSTRAINT lors_complaintphoto_pkey PRIMARY KEY (id);


--
-- Name: lors_review lors_review_pkey; Type: CONSTRAINT; Schema: public; Owner: lors_user
--

ALTER TABLE ONLY public.lors_review
    ADD CONSTRAINT lors_review_pkey PRIMARY KEY (id);


--
-- Name: lors_sitesettings lors_sitesettings_pkey; Type: CONSTRAINT; Schema: public; Owner: lors_user
--

ALTER TABLE ONLY public.lors_sitesettings
    ADD CONSTRAINT lors_sitesettings_pkey PRIMARY KEY (id);


--
-- Name: auth_group_name_a6ea08ec_like; Type: INDEX; Schema: public; Owner: lors_user
--

CREATE INDEX auth_group_name_a6ea08ec_like ON public.auth_group USING btree (name varchar_pattern_ops);


--
-- Name: auth_group_permissions_group_id_b120cbf9; Type: INDEX; Schema: public; Owner: lors_user
--

CREATE INDEX auth_group_permissions_group_id_b120cbf9 ON public.auth_group_permissions USING btree (group_id);


--
-- Name: auth_group_permissions_permission_id_84c5c92e; Type: INDEX; Schema: public; Owner: lors_user
--

CREATE INDEX auth_group_permissions_permission_id_84c5c92e ON public.auth_group_permissions USING btree (permission_id);


--
-- Name: auth_permission_content_type_id_2f476e4b; Type: INDEX; Schema: public; Owner: lors_user
--

CREATE INDEX auth_permission_content_type_id_2f476e4b ON public.auth_permission USING btree (content_type_id);


--
-- Name: auth_user_groups_group_id_97559544; Type: INDEX; Schema: public; Owner: lors_user
--

CREATE INDEX auth_user_groups_group_id_97559544 ON public.auth_user_groups USING btree (group_id);


--
-- Name: auth_user_groups_user_id_6a12ed8b; Type: INDEX; Schema: public; Owner: lors_user
--

CREATE INDEX auth_user_groups_user_id_6a12ed8b ON public.auth_user_groups USING btree (user_id);


--
-- Name: auth_user_user_permissions_permission_id_1fbb5f2c; Type: INDEX; Schema: public; Owner: lors_user
--

CREATE INDEX auth_user_user_permissions_permission_id_1fbb5f2c ON public.auth_user_user_permissions USING btree (permission_id);


--
-- Name: auth_user_user_permissions_user_id_a95ead1b; Type: INDEX; Schema: public; Owner: lors_user
--

CREATE INDEX auth_user_user_permissions_user_id_a95ead1b ON public.auth_user_user_permissions USING btree (user_id);


--
-- Name: auth_user_username_6821ab7c_like; Type: INDEX; Schema: public; Owner: lors_user
--

CREATE INDEX auth_user_username_6821ab7c_like ON public.auth_user USING btree (username varchar_pattern_ops);


--
-- Name: django_admin_log_content_type_id_c4bce8eb; Type: INDEX; Schema: public; Owner: lors_user
--

CREATE INDEX django_admin_log_content_type_id_c4bce8eb ON public.django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_user_id_c564eba6; Type: INDEX; Schema: public; Owner: lors_user
--

CREATE INDEX django_admin_log_user_id_c564eba6 ON public.django_admin_log USING btree (user_id);


--
-- Name: django_session_expire_date_a5c62663; Type: INDEX; Schema: public; Owner: lors_user
--

CREATE INDEX django_session_expire_date_a5c62663 ON public.django_session USING btree (expire_date);


--
-- Name: django_session_session_key_c0390e0f_like; Type: INDEX; Schema: public; Owner: lors_user
--

CREATE INDEX django_session_session_key_c0390e0f_like ON public.django_session USING btree (session_key varchar_pattern_ops);


--
-- Name: lors_brand_name_aa56162e_like; Type: INDEX; Schema: public; Owner: lors_user
--

CREATE INDEX lors_brand_name_aa56162e_like ON public.lors_brand USING btree (name varchar_pattern_ops);


--
-- Name: lors_carmodel_brand_id_00a4ade4; Type: INDEX; Schema: public; Owner: lors_user
--

CREATE INDEX lors_carmodel_brand_id_00a4ade4 ON public.lors_carmodel USING btree (brand_id);


--
-- Name: lors_complaint_car_model_id_051e12ce; Type: INDEX; Schema: public; Owner: lors_user
--

CREATE INDEX lors_complaint_car_model_id_051e12ce ON public.lors_complaint USING btree (car_model_id);


--
-- Name: lors_complaintphoto_complaint_id_c92316d9; Type: INDEX; Schema: public; Owner: lors_user
--

CREATE INDEX lors_complaintphoto_complaint_id_c92316d9 ON public.lors_complaintphoto USING btree (complaint_id);


--
-- Name: auth_group_permissions auth_group_permissio_permission_id_84c5c92e_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: lors_user
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissions_group_id_b120cbf9_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: lors_user
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_permission auth_permission_content_type_id_2f476e4b_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: lors_user
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups auth_user_groups_group_id_97559544_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: lors_user
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_group_id_97559544_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups auth_user_groups_user_id_6a12ed8b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: lors_user
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_6a12ed8b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: lors_user
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: lors_user
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_content_type_id_c4bce8eb_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: lors_user
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_user_id_c564eba6_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: lors_user
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: lors_carmodel lors_carmodel_brand_id_00a4ade4_fk_lors_brand_id; Type: FK CONSTRAINT; Schema: public; Owner: lors_user
--

ALTER TABLE ONLY public.lors_carmodel
    ADD CONSTRAINT lors_carmodel_brand_id_00a4ade4_fk_lors_brand_id FOREIGN KEY (brand_id) REFERENCES public.lors_brand(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: lors_complaint lors_complaint_car_model_id_051e12ce_fk_lors_carmodel_id; Type: FK CONSTRAINT; Schema: public; Owner: lors_user
--

ALTER TABLE ONLY public.lors_complaint
    ADD CONSTRAINT lors_complaint_car_model_id_051e12ce_fk_lors_carmodel_id FOREIGN KEY (car_model_id) REFERENCES public.lors_carmodel(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: lors_complaintphoto lors_complaintphoto_complaint_id_c92316d9_fk_lors_complaint_id; Type: FK CONSTRAINT; Schema: public; Owner: lors_user
--

ALTER TABLE ONLY public.lors_complaintphoto
    ADD CONSTRAINT lors_complaintphoto_complaint_id_c92316d9_fk_lors_complaint_id FOREIGN KEY (complaint_id) REFERENCES public.lors_complaint(id) DEFERRABLE INITIALLY DEFERRED;


--
-- PostgreSQL database dump complete
--

\unrestrict zB4aminOi4xmJF2dYyQhcKehc1WElsIRfuqERc4E8vbSRh5j1B0entC1lw7SmmC

