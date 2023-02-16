from abc import abstractmethod, ABC

PLAY_STORE_BASE_URL = "https://play.google.com"


class Format(ABC):
    @abstractmethod
    def build(self, *args):
        raise NotImplementedError

    @abstractmethod
    def build_body(self, *args):
        raise NotImplementedError


class Formats:
    class _Detail(Format):
        URL_FORMAT = "{}/store/apps/details?id={{app_id}}&hl={{lang}}&gl={{country}}".format(
            PLAY_STORE_BASE_URL
        )
        FALLBACK_URL_FORMAT = "{}/store/apps/details?id={{app_id}}&hl={{lang}}".format(
            PLAY_STORE_BASE_URL
        )

        def build(self, app_id: str, lang: str, country: str) -> str:
            return self.URL_FORMAT.format(app_id=app_id, lang=lang, country=country)

        def fallback_build(self, app_id: str, lang: str) -> str:
            return self.FALLBACK_URL_FORMAT.format(app_id=app_id, lang=lang)

        def build_body(self, *args):
            return None

    class _Reviews(Format):
        URL_FORMAT = "{}/_/PlayStoreUi/data/batchexecute?hl={{lang}}&gl={{country}}".format(
            PLAY_STORE_BASE_URL
        )

        def build(self, lang: str, country: str) -> str:
            return self.URL_FORMAT.format(lang=lang, country=country)

        PAYLOAD_FORMAT_FOR_FIRST_PAGE = "f.req=%5B%5B%5B%22UsvDTd%22%2C%22%5Bnull%2Cnull%2C%5B2%2C{sort}%2C%5B{count}%2Cnull%2Cnull%5D%2Cnull%2C%5Bnull%2C{score}%5D%5D%2C%5B%5C%22{app_id}%5C%22%2C{store_id}%5D%5D%22%2Cnull%2C%22generic%22%5D%5D%5D"
        PAYLOAD_FORMAT_FOR_PAGINATED_PAGE = "f.req=%5B%5B%5B%22UsvDTd%22%2C%22%5Bnull%2Cnull%2C%5B2%2C{sort}%2C%5B{count}%2Cnull%2C%5C%22{pagination_token}%5C%22%5D%2Cnull%2C%5Bnull%2C{score}%5D%5D%2C%5B%5C%22{app_id}%5C%22%2C{store_id}%5D%5D%22%2Cnull%2C%22generic%22%5D%5D%5D"

        PAYLOAD_FORMAT_FOR_BOOKS_FIRST_PAGE = "f.req=%5B%5B%5B%22oCPfdb%22%2C%22%5Bnull%2C%5B2%2C{sort}%2C%5B{count}%2Cnull%2Cnull%5D%2Cnull%2C%5Bnull%2C{score}%5D%5D%2C%5B%5C%22{app_id}%5C%22%2C{store_id}%5D%5D%22%2Cnull%2C%22generic%22%5D%5D%5D"
        PAYLOAD_FORMAT_FOR_BOOKS_PAGINATED_PAGE = "f.req=%5B%5B%5B%22oCPfdb%22%2C%22%5Bnull%2C%5B2%2C{sort}%2C%5B{count}%2Cnull%2C%5C%22{pagination_token}%5C%22%5D%2Cnull%2C%5Bnull%2C{score}%5D%5D%2C%5B%5C%22{app_id}%5C%22%2C{store_id}%5D%5D%22%2Cnull%2C%22generic%22%5D%5D%5D"

        def build_body(
            self,
            store_id: int,
            app_id: str,
            sort: int,
            count: int,
            filter_score_with: int,
            pagination_token: str,
        ) -> bytes:
            if store_id == 9:
                paginated_format = self.PAYLOAD_FORMAT_FOR_BOOKS_PAGINATED_PAGE
                first_page_format = self.PAYLOAD_FORMAT_FOR_BOOKS_FIRST_PAGE
            else:
                paginated_format = self.PAYLOAD_FORMAT_FOR_PAGINATED_PAGE
                first_page_format = self.PAYLOAD_FORMAT_FOR_FIRST_PAGE

            if pagination_token is not None:
                result = paginated_format.format(
                    store_id=store_id,
                    app_id=app_id,
                    sort=sort,
                    count=count,
                    score=filter_score_with,
                    pagination_token=pagination_token,
                )
            else:
                result = first_page_format.format(
                    store_id=store_id, app_id=app_id, sort=sort, score=filter_score_with, count=count
                )

            return result.encode()

    class _Permissions(Format):
        URL_FORMAT = "{}/_/PlayStoreUi/data/batchexecute?hl={{lang}}&gl={{country}}".format(
            PLAY_STORE_BASE_URL
        )

        def build(self, lang: str, country: str) -> str:
            return self.URL_FORMAT.format(lang=lang, country=country)

        PAYLOAD_FORMAT_FOR_PERMISSION = "f.req=%5B%5B%5B%22xdSrCf%22%2C%22%5B%5Bnull%2C%5B%5C%22{app_id}%5C%22%2C{store_id}%5D%2C%5B%5D%5D%5D%22%2Cnull%2C%221%22%5D%5D%5D"

        def build_body(self, store_id: int, app_id: str) -> bytes:
            result = self.PAYLOAD_FORMAT_FOR_PERMISSION.format(store_id=store_id, app_id=app_id)

            return result.encode()

    class _Searchresults(Format):
        URL_FORMAT = "{}/store/search?q={{query}}&c=apps&hl={{lang}}&gl={{country}}".format(
            PLAY_STORE_BASE_URL
        )
        FALLBACK_URL_FORMAT = "{}/store/search?q={{query}}&c=apps&hl={{lang}}".format(
            PLAY_STORE_BASE_URL
        )

        def build(self, query: str, lang: str, country: str) -> str:
            return self.URL_FORMAT.format(query=query, lang=lang, country=country)

        def fallback_build(self, query: str, lang: str) -> str:
            return self.FALLBACK_URL_FORMAT.format(query=query, lang=lang)

        def build_body(self, *args):
            return None

    Detail = _Detail()
    Reviews = _Reviews()
    Permissions = _Permissions()
    Searchresults = _Searchresults()
